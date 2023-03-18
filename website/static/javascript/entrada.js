    // Denotes total number of rows
    var rowIdx = 0;
    var total = 0;
    
    // jQuery button click event to add a row
    $('#addBtn').on('click', function () {
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
                <input type="hidden" value="${$('#costo').val()}" name="costoR${rowIdx}">
                ${$('#costo').val()}
              </td>
              <td class="text-center">
                <button class="btn btn-danger btn-sm remove" type="button"><i class="bi bi-x-circle"></i></button>
              </td>
            </tr>`);
            total += parseInt($('#cantidad').val())*parseInt($('#costo').val());
            $('#total').text(total);
            $('#cantidad').val('');
            $('#producto').val('');
            $('#monto_total').val(total);

            new AutoNumeric.multiple('.formato', {
              allowDecimalPadding: false,
              unformatOnSubmit: true,
              decimalCharacter : '.',
              digitGroupSeparator : ',',
            });
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
    
    $(document).ready(function(){
      $('#tabla-productos').DataTable( {
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
    
    $(document).on('click', '.cancel', function(){
      location.reload();
    });
    
    $(document).ready(function(){
      $('#ci-ruc').focus();
    });

    const en_formatter = new Intl.NumberFormat('es-ES', {maximumFractionDigits: 0 });

    new AutoNumeric.multiple('.formatear', {
      allowDecimalPadding: false,
      unformatOnSubmit: true,
      decimalCharacter : '.',
      digitGroupSeparator : ',',
    });
    