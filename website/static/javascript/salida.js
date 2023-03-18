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
          url:"/selectproducto2",
          method:"POST",
          data:{prod:prod},
          success:function(data){
            var data_rs = JSON.parse(data);
            data_rs.forEach(linea => {
            // Adding a row inside the tbody.
            $('#tbody').append(`
            <tr id="R${++rowIdx}">
              <td class="row-index">
                <input type="hidden" value="${linea['cantidad']}" name="cantidadR${rowIdx}">
                ${linea['cantidad']}
              </td>
              <td class="row-index">
                <input type="hidden" value="${linea['producto']}" name="productoR${rowIdx}">
                ${linea['descripcion']}
              </td>
              <td class="row-index">
                <input type="hidden" value="${linea['costo']}" name="costoR${rowIdx}">
                ${en_formatter.format(linea['costo'])}
              </td>
              <td class="text-center">
                <button class="btn btn-danger btn-sm remove" type="button"><i class="bi bi-x-circle"></i></button>
              </td>
            </tr>`);
            total += parseInt(linea['cantidad'])*parseInt(linea['costo']);
            $('#total').text(en_formatter.format(total));
            $('#monto-total').val(total);
            $('#cantidad').val('');
            $('#producto').val(''); 
            $('#costo').val(''); 
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
      decimalCharacter : ',',
      digitGroupSeparator : '.',
    });