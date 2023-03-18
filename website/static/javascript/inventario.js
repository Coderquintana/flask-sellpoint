$(document).ready(function () {
  $('#inventario').DataTable({
    initComplete: function () {
      this.api()
      .columns([3,4])
      .every(function () {
          var column = this;
          console.log(this.columns([4]))
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
});
$(document).ready(function() {
  $('.myselect').select2({
    placeholder: "Filtrar",
    allowClear: true
  });
});

 type="text/javascript">
$(function() {
  $('input[name="daterange"]').daterangepicker();
});

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