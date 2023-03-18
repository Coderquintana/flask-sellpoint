$(document).ready(function () {
  $('#facturas').DataTable({
    initComplete: function () {
      this.api()
        .columns([1,2,3,5])
        .every(function () {
          var column = this;
          var select = $('<select class="myselect"><option value=""></option></select>')
          .appendTo( $(column.header()) )
          .on('change', function () {
            var val = $.fn.dataTable.util.escapeRegex($(this).val());
            column.search(val ? '^' + val + '$' : '', true, false).draw();
          });

          column
          .data()
          .unique()
          .sort()
          .each(function (d, j) {
            select.append('<option value="' + d + '">' + d + '</option>');
          });
        });
      },
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
  var minDate, maxDate;

  // Custom filtering function which will search data in column four between two values
  $.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
      var min = minDate.val();
      var max = maxDate.val();
      var date = data[5];

      if (
          ( min === null && max === null ) ||
          ( min === null && date <= max ) ||
          ( min <= date   && max === null ) ||
          ( min <= date   && date <= max )
      ) {
          return true;
      }
      return false;
    }
  );

  // Create date inputs
  minDate = $('#desde');
  maxDate = $('#hasta');

  // DataTables initialisation
  var table = $('#facturas').DataTable();

  // Refilter the table
  $('#desde, #hasta').on('change', function () {
      table.draw();
  });

  $('.myselect').select2({
    placeholder: "Filtrar",
    allowClear: true
  });

  new AutoNumeric.multiple('.formato', {
    allowDecimalPadding: false,
    unformatOnSubmit: true,
    decimalCharacter : ',',
    digitGroupSeparator : '.',
  });
  
});

  
$('.mostrar').on('click', function(){
  $('#mostrar').modal('show');
  var id = $(this).attr('id');
  $.ajax({
    url:"/selectfactura",
    method:"POST",
    data:{id:id},
    success:function(data){
      var data_rs = JSON.parse(data);
      $('#modal-bodyy').html(`
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col" class="border-0 text-uppercase font-medium">Nro Factura</th>
              <th scope="col" class="border-0 text-uppercase font-medium">Cliente</th>
              <th scope="col" class="border-0 text-uppercase font-medium">Total</th>
              <th scope="col" class="border-0 text-uppercase font-medium">Estado</th>
              <th scope="col" class="border-0 text-uppercase font-medium">Delivery</th>
              <th scope="col" class="border-0 text-uppercase font-medium">Telefono</th>
              <th scope="col" class="border-0 text-uppercase font-medium">POS</th>
              <th scope="col" class="border-0 text-uppercase font-medium">Nro Cuenta</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>${data_rs[0]['nro_factura']}</td>
              <td>${data_rs[0]['cliente']}</td>
              <td>${en_formatter.format(data_rs[0]['monto_total'])} G</td>
              <td>${data_rs[0]['estado']}</td>
              <td>${data_rs[0]['delivery_ci']}</td>
              <td>${data_rs[0]['delivery_phone']}</td>
              <td>${data_rs[0]['pos']}</td>
              <td>${data_rs[0]['nro_cuenta']}</td>
            </tr>
          </tbody>
          <table class="table table-striped">
            <thead class="table-group-divider">
              <tr>
                <th scope="col" class="border-0 text-uppercase font-medium pl-4">Producto</th>
                <th scope="col" class="border-0 text-uppercase font-medium">Cantidad</th>
                <th scope="col" class="border-0 text-uppercase font-medium">Precio</th>
              </tr>
            </thead>
            <tbody id="detalles">
              
            </tbody>
      `);
        var facturaid = data_rs[0]['id'];
        $.ajax({
          url:"/selectdetallefactura",
          method:"POST",
          data:{facturaid:facturaid},
          success:function(data){
            var data_rs2 = JSON.parse(data);

            data_rs2.forEach(linea => {
              $('#detalles').append(`
                <tr>
                  <td>${linea['id_producto']}</td>
                  <td>${linea['cantidad']}</td>
                  <td>${en_formatter.format(linea['precio'])}G</td>
                </tr>
              `);
            });
          }
        });
    }
  });
});
  
const en_formatter = new Intl.NumberFormat('es-ES', {maximumFractionDigits: 0 });
  
document.getElementById("btnExport").onclick = function () {
  printElement(document.getElementById("printThis"));
}

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
  location.reload();
}


