$(document).on('change', '.view_proveedor', function(){
  var ci_ruc = $(this).val();
  $.ajax({
    url:"/selectproveedor",
    method:"POST",
    data:{ci_ruc:ci_ruc},
    success:function(data){
      var data_rs = JSON.parse(data);
      $('#name').val(data_rs[0]['name']);
    }
  });

  $.ajax({
    url:"/selectfactura_com",
    method:"POST",
    data:{ci_ruc:ci_ruc},
    success:function(data){
      var data_rs = JSON.parse(data);
      $('#nro_factura_compra').val(data_rs[0]['nro_factura_compra']);
      $('#fecha').val(data_rs[0]['fecha']);
      $('#monto_total').val(data_rs[0]['monto_total']);
      $('#saldo_factura').val(data_rs[0]['saldo_factura']);
    }
  });
});



new AutoNumeric.multiple('.formato', {
    allowDecimalPadding: false,
    unformatOnSubmit: true,
    decimalCharacter : ',',
    digitGroupSeparator : '.',
    });  
   
$(document).ready(function () {
    $('#pagos').DataTable( {
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
  $('#confirmar').prop('hidden', true);
  $('#cerrar').prop('hidden', true);
  $('#saldo_factura').prop('hidden', true);
  printElement(document.getElementById("pago-form-modal"));
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