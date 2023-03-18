$(document).ready(function(){
  $(document).on('change', '.view_proveedor', function(){
    var ci_ruc = $(this).val();
    $.ajax({
      url:"/selectproveedor",
      method:"POST",
      data:{ci_ruc:ci_ruc},
      success:function(data){
        var data_rs = JSON.parse(data);
        $('#name').val(data_rs[0]['name']);
        $('#phone').val(data_rs[0]['phone']);
        $('#address').val(data_rs[0]['address']);
        $('#email').val(data_rs[0]['email']);
        $('#city').val(data_rs[0]['city']);
        $('#name').prop('readonly', true);
        $('#phone').prop('readonly', true);
        $('#address').prop('readonly', true);
        $('#email').prop('readonly', true);
        $('#ci-ruc').prop('readonly', true);
        $('#modif').prop('hidden',false);
      }
    });
  });
  $(document).on('click', '.view_proveedor', function(){
    if ($(this).is('[readonly]')){
      console.log('llego aquí')
      var result = confirm ('Cambiar Proveedor');
      if (result == false){
        event.preventDefault();
      }else{
        $('#name').val("");
        $('#phone').val("");
        $('#address').val("");
        $('#email').val("");
        $('#ci-ruc').val("");
        $('#city').val("");
        $('#name').prop('readonly', false);
        $('#phone').prop('readonly', false);
        $('#address').prop('readonly', false);
        $('#email').prop('readonly', false);
        $('#ci-ruc').prop('readonly', false);
        $('#city').prop('readonly', false);
        $('#modif').prop('hidden',true);
      }
    }
  });
});

$(document).ready(function(){
  $(document).on('change', '.view_compra', function(){
    var prod = $(this).val();
    $.ajax({
      url:"/selectproductocompra",
      method:"POST",
      data:{prod:prod},
      success:function(data){
        var data_rs = JSON.parse(data);
        $('#producto').val(data_rs[0]['descripcion']);
        $('#costo').val(data_rs[0]['costo']);
        $('#producto').prop('readonly', false);
        $('#costo').prop('readonly', false);
      }
    });
  });
});  
// Denotes total number of rows
var rowIdx = 0;
var total = 0;

// jQuery button click event to add a row
$('#addBtn').on('click', function () {
  if($('#cantidad').val() == ''){
    alert("Seleccione Cantidad")
  }else if ($('#producto').val() == ''){
    alert("Seleccione Producto")
  }else if ($('#costo').val() == ''){
    alert("Agregar Costo")
  }else{
    var prod = $('#producto').val();
    $.ajax({
      url:"/selectproductocompra",
      method:"POST",
      data:{prod:prod},
      success:function(data){
        var data_rs = JSON.parse(data);
        var costo = parseInt($('#costo').val());
        var cant = parseInt($('#cantidad').val());
        // Adding a row inside the tbody.
        $('#tbody').append(`
        <tr id="R${++rowIdx}">
          <td class="row-index">
            <input type="hidden" value="${cant}" name="cantidadR${rowIdx}">
            ${cant}
          </td>
          <td class="row-index">
            <input type="hidden" value="${$('#unidad_medida').val()}" name="unidad_medidaR${rowIdx}">
            ${$('#unidad_medida').val()}
          </td>
          <td class="row-index">
            <input type="hidden" value="${$('#producto').val()}" name="productoR${rowIdx}">
            ${$('#producto').val()}
          </td>
          <td class="row-index">
            <input type="hidden" value="${costo}" name="costoR${rowIdx}">
            ${en_formatter.format(costo)}
          </td>
          <td class="row-index" id="subtotal" name="subtotal">
            ${en_formatter.format(cant * parseInt(costo))}
          </td>
          <td class="text-center">
            <button class="btn btn-danger btn-sm remove" type="button"><i class="bi bi-x-circle"></i></button>
          </td>
        </tr>`);
        total += cant*parseInt(costo);
        $('#total').text(en_formatter.format(total));
        $('#cantidad').val('');
        $('#producto').val('');
        $('#costo').val('');
        $('#unidad_medida').val('');
      }
    });
  }
  });

// jQuery button click event to remove a row.
$('#tbody').on('click', '.remove', function () {

// Getting all the rows next to the row
// containing the clicked button
var child = $(this).closest('tr').nextAll();    

var linea = parseInt($(this).closest('tr').find('#subtotal').text());

// Iterating across all the rows 
// obtained to change the index
child.each(function () {

  // Getting <tr> id.
  var id = $(this).attr('id');

  // Getting the <p> inside the .row-index class.
  var idx = $(this).children('.row-index').children('p');

  // Gets the row number from <tr> id.
  var dig = parseInt(id.substring(1));

  // Modifying row index.
  idx.html(`Row ${dig - 1}`);

  // Modifying row id.
  $(this).attr('id', `R${dig - 1}`);
});

// Removing the current row.
$(this).closest('tr').remove();

// Decreasing total number of rows by 1.
rowIdx--;

// Decreasin total value
$('#total').text(parseInt($('#total').text())-linea);
total = total - linea;
$('#monto-total').val(parseInt($('#monto-total').val())-linea);
});

$('#modif').on('click', function(){
$('#name').prop('readonly', false);
$('#phone').prop('readonly', false);
$('#address').prop('readonly', false);
$('#email').prop('readonly', false);
$('#modif').prop('hidden',true);
});

$(document).ready(function(){
$('#tabla-ordencompra').DataTable( {
  language: {
  "decimal": "",
  "emptyTable": "No hay información",
  "info": "Mostrando _START_ a _END_ de _TOTAL_",
  "infoEmpty": "Mostrando 0 to 0 of 0",
  "infoFiltered": "(Filtrado de _MAX_ total)",
  "infoPostFix": "",
  "thousands": ",",
  "lengthMenu": "Mostrar _MENU_ ",
  "loadingRecords": "Cargando...",
  "processing": "Procesando...",
  "search": "Buscar:",
  "zeroRecords": "Sin resultados encontrados",
  "paginate": {
       "first": "primero",
       "last": "Ultimo",
       "next": "Siguiente",
       "previous": "Anterior" }
  }
});
});

$(document).on('click', '.buscar-ordencompra', function (){
$('#modalordencompra').show();
});

$(document).on('click', '.carga_ordencompra', function() {
  var orden_compra = $(this).attr("id");
  $.ajax({
    url:"/selectordencompra",
    method:"POST",
    data:{orden_compra:orden_compra},
    success:function(data){
      var data_rs = JSON.parse(data);
      $('#ci-ruc').val(data_rs[0]['ci_ruc']);
      $('#descripcion').val(data_rs[0]['descripcion']);
      var ci_ruc = data_rs[0]['ci_ruc'];
        $.ajax({
          url:"/selectproveedor",
          method:"POST",
          data:{ci_ruc:ci_ruc},
          success:function(data){
  
            var data_rs2 = JSON.parse(data);
            var x = new Date(data_rs[0]['fecha_pago']);
            let entrega = x.getFullYear() +'-'+(x.getMonth()+1) + '-' + (x.getDate()+1);
  
            $('#name').val(data_rs2[0]['name']);
            $('#phone').val(data_rs2[0]['phone']);
            $('#address').val(data_rs2[0]['address']);
            $('#email').val(data_rs2[0]['email']);
            $('#city').val(data_rs2[0]['city']);
            $(".d-flex h3").html("Modificar Orden Compra " + orden_compra);
            $('#id').val(orden_compra);
            $('#fecha').val(entrega);
            $('#name').prop('readonly', true);
            $('#city').prop('readonly', true);
            $('#phone').prop('readonly', true);
            $('#address').prop('readonly', true);
            $('#email').prop('readonly', true);
            $('#ci-ruc').prop('readonly', true);
            $('#modif').prop('hidden',false);
            $('#cancel').prop('hidden',false);
            $('#modif-ordencompra').prop('hidden',false);
            $('#confirmar').prop('hidden', true);
          }
        });
        $.ajax({
          url:"/selectdetalleordencompra",
          method:"POST",
          data:{orden_compra:orden_compra},
          success:function(data){
  
            var data_rs3 = JSON.parse(data);
            data_rs3.forEach(linea => {
              console.log(linea)
  
              $('#tbody').append(`
                <tr id="R${++rowIdx}">
                  <td class="row-index">
                    <input type="hidden" value="${linea['cantidad']}" name="cantidadR${rowIdx}">
                    ${linea['cantidad']}
                  </td>
                  <td class="row-index">
                    <input type="hidden" value="${linea['unidad_medida']}" name="unidad_medidaR${rowIdx}">
                    ${linea['unidad_medida']}
                  </td>
                  <td class="row-index">
                    <input type="hidden" value="${linea['descripcion']}" name="productoR${rowIdx}">
                    ${linea['descripcion']}
                  </td>
                  <td class="row-index">
                    <input type="hidden" value="${linea['precio']}" name="costoR${rowIdx}">
                    ${en_formatter.format(linea['precio'])}
                  </td>
                  <td class="row-index" id="subtotal" name="subtotal">
                  ${en_formatter.format(linea['cantidad']*linea['precio'])}
                  </td>
                  <td class="text-center">
                    <button class="btn btn-danger btn-sm remove" type="button"><i class="bi bi-x-circle"></i></button>
                  </td>
                </tr>`);
                total += parseInt(linea['cantidad'])*parseInt(linea['precio']);
                $('#total').text(en_formatter.format(total));
                $('#monto-total').val(total);
                $('#cantidad').val('');
                $('#producto').val('');   
            });
          }
        });               
      $('#modalordencompra').hide();
      $('.modal-backdrop').remove();
      $('body').removeClass("modal-open");
    }
  });
  });

$('#unidad_medida').on('change', function(){
  if($('#unidad_medida').val() == 'Unidad'){
    varcosto=parseInt($('#costo').val())*1;
    $('#costo').val(varcosto);
  }else if($('#unidad_medida').val() == 'Caja x 5 unid'){
   varcosto5=parseInt($('#costo').val())*5;
   $('#costo').val(varcosto5);
  }else if ($('#unidad_medida').val() == 'Caja x 10 unid'){
    varcosto10=parseInt($('#costo').val())*10;
    $('#costo').val(varcosto10);
  }else if ($('#unidad_medida').val() == 'Caja x 12 unid'){
    varcosto12=parseInt($('#costo').val())*12;
    $('#costo').val(varcosto12);
  } 
});



new AutoNumeric('.formato', {

allowDecimalPadding: false,
unformatOnSubmit: true,
decimalCharacter : ',',
digitGroupSeparator : '.',
});

const en_formatter = new Intl.NumberFormat('es-ES', {maximumFractionDigits: 0 });

$(document).ready(function () {
  $('#orden_compras').DataTable( {
       language: {
       "decimal": "",
       "emptyTable": "No hay información",
       "info": "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
       "infoEmpty": "Mostrando 0 to 0 of 0 Entradas",
       "infoFiltered": "(Filtrado de _MAX_ total entradas)",
       "infoPostFix": "",
       "thousands": ",",
       "lengthMenu": "Mostrar _MENU_ Entradas",
       "loadingRecords": "Cargando...",
       "processing": "Procesando...",
       "search": "Buscar:",
       "zeroRecords": "Sin resultados encontrados",
       "paginate": {
            "first": "primero",
            "last": "Ultimo",
            "next": "Siguiente",
            "previous": "Anterior" }
       }
  });
});

$('#confirmar').on('click', function(e){
  $('#containerdet').prop('hidden', true);
  $('#noimprimir').prop('hidden', true);
  printElement(document.getElementById("printThis"));
  location.reload();
});

function printElement(elem) {
  var domClone = elem.cloneNode(true);
  
  var $printSection = document.getElementById("printSection");
  
  if (!$printSection) {
    var $printSection = document.createElement("div");
    $printSection.id = "printSection";
    document.body.appendChild($printSection);
  }
  
  $printSection.innerHTML = "";
  $printSection.appendChild(domClone);
  window.print();
}