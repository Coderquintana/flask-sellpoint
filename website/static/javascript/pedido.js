$(document).on('change', '.view_cliente', function(){
  var ci_ruc = $(this).val();
  $.ajax({
    url:"/selectcliente",
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
      $('#city').prop('readonly', true);
      $('#phone').prop('readonly', true);
      $('#address').prop('readonly', true);
      $('#email').prop('readonly', true);
      $('#ci-ruc').prop('readonly', true);
      $('#modif').prop('hidden',false);
      $('#producto').focus();
    }
  });
});
$(document).on('click', '.view_cliente', function(){
  if ($(this).is('[readonly]')){
    var result = confirm ('Cambiar Cliente');
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
      $('#city').prop('readonly', false);
      $('#phone').prop('readonly', false);
      $('#address').prop('readonly', false);
      $('#email').prop('readonly', false);
      $('#ci-ruc').prop('readonly', false);
      $('#modif').prop('hidden',true);
    }
  }
});

// Denotes total number of rows
var rowIdx = 0;
var total = 0;

// jQuery button click event to add a row
$('#cantidad').on('change', function () {
  if($('#cantidad').val() == ''){
    alert("Seleccione Cantidad")
  }else if ($('#producto').val() == ''){
    alert("Seleccione Producto")
  }else{
    var prod = $('#producto').val();
    $.ajax({
      url:"/selectproducto",
      method:"POST",
      data:{prod:prod},
      success:function(data){
        var data_rs = JSON.parse(data);
        // Adding a row inside the tbody.
        $('#tbody').append(`
        <tr id="R${++rowIdx}">
          <td class="row-index">
            <input type="hidden" value="${$('#cantidad').val()}" name="cantidadR${rowIdx}">
            ${$('#cantidad').val()}
          </td>
          <td class="row-index">
            <input type="hidden" value="${$('#producto').val()}" name="productoR${rowIdx}">
            ${$('#producto').val()}
          </td>
          <td class="row-index">
            <input type="hidden" value="${data_rs[0]['precio1']}" name="precioR${rowIdx}">
            ${data_rs[0]['precio1']}
          </td>
          <td class="row-index" id="subtotal" name="subtotal">
            ${parseInt($('#cantidad').val()) * parseInt(data_rs[0]['precio1'])}
          </td>
          <td class="text-center">
            <button class="btn btn-danger btn-sm remove" type="button"><i class="bi bi-x-circle"></i></button>
          </td>
        </tr>`);
        total += parseInt($('#cantidad').val())*parseInt(data_rs[0]['precio1']);
        $('#total').text(total);
        $('#cantidad').val('');
        $('#producto').val('');
        $('#producto').focus();
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
});

$('#modif').on('click', function(){
  $('#name').prop('readonly', false);
  $('#phone').prop('readonly', false);
  $('#address').prop('readonly', false);
  $('#email').prop('readonly', false);
  $('#modif').prop('hidden',true);
});

$(document).ready(function(){
  $('#tabla-pedidos').DataTable( {
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


$(document).on('click', '.buscar-pedido', function (){
  $('#modalpedido').show();
});

$(document).on('click', '.carga_pedido', function() {
  var pedido = $(this).attr("id");
  $.ajax({
    url:"/selectpedido",
    method:"POST",
    data:{pedido:pedido},
    success:function(data){
      var data_rs = JSON.parse(data);
      $('#ci-ruc').val(data_rs[0]['ci_ruc']);
      var ci_ruc = data_rs[0]['ci_ruc'];
        $.ajax({
          url:"/selectcliente",
          method:"POST",
          data:{ci_ruc:ci_ruc},
          success:function(data){

            var data_rs2 = JSON.parse(data);
            var x = new Date(data_rs[0]['fecha_entrega']);
            let entrega = x.getFullYear() +'-'+(x.getMonth()+1) + '-' + (x.getDate()+1);

            $('#name').val(data_rs2[0]['name']);
            $('#phone').val(data_rs2[0]['phone']);
            $('#address').val(data_rs2[0]['address']);
            $('#email').val(data_rs2[0]['email']);
            $('#city').val(data_rs2[0]['city']);
            $(".d-flex h3").html("Modificar Pedido " + pedido);
            $('#sgte-pedido').val(pedido);
            $('#fecha-entrega').val(entrega);
            $('#name').prop('readonly', true);
            $('#city').prop('readonly', true);
            $('#phone').prop('readonly', true);
            $('#address').prop('readonly', true);
            $('#email').prop('readonly', true);
            $('#ci-ruc').prop('readonly', true);
            $('#modif').prop('hidden',false);
            $('#cancel').prop('hidden',false);
            $('#modif-pedido').prop('hidden',false);
            $('#confirmar').prop('hidden', true);
          }
        });
        $.ajax({
          url:"/selectdetalle",
          method:"POST",
          data:{pedido:pedido},
          success:function(data){

            var data_rs3 = JSON.parse(data);
            data_rs3.forEach(linea => {

              $('#tbody').append(`
                <tr id="R${++rowIdx}">
                  <td class="row-index">
                    <input type="hidden" value="${linea['cantidad']}" name="cantidadR${rowIdx}">
                    ${linea['cantidad']}
                  </td>
                  <td class="row-index">
                    <input type="hidden" value="${linea['codigo']}" name="productoR${rowIdx}">
                    ${linea['codigo']}
                  </td>
                  <td class="row-index">
                    <input type="hidden" value="${linea['precio']}" name="precioR${rowIdx}">
                    ${linea['precio']}
                  </td>
                  <td class="row-index" id="subtotal" name="subtotal">
                    ${linea['cantidad']*linea['precio']}
                  </td>
                  <td class="text-center">
                    <button class="btn btn-danger btn-sm remove" type="button"><i class="bi bi-x-circle"></i></button>
                  </td>
                </tr>`);
                total += linea['cantidad']*linea['precio'];
                $('#total').text(total);
                $('#cantidad').val('');
                $('#producto').val('');
            });
          }
        });               
      $('#modalpedido').hide();
      $('.modal-backdrop').remove();
      $('body').removeClass("modal-open");
    }
  });
});

$(document).on('click', '.cancel', function(){
  location.reload();
});

$(document).ready(function(){
  $('#ci-ruc').focus();
});
