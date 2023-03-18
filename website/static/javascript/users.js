function showAlert(){
     var result = confirm ('Esta seguro que desea eliminar?');
     if (result == false){
          event.preventDefault();
          btn.blur();
     }
}

$(document).ready(function () {
     $('#users').DataTable( {
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

$(document).ready(function(){

     $(document).on('click', '.view_data', function(){
          var user_id = $(this).attr("id");
          $.ajax({
               url:"/select",
               method:"POST",
               data:{user_id:user_id},
               success:function(data){
                         $('#add-user-permission').modal('show');
                         var data_rs = JSON.parse(data);
                         $('#edit_id').val(data_rs[0]['id']);
               }
          });
     });
}); 

// document.getElementById('btnEliminar').addEventListener('click', function(e) {
//      var result = confirm('Esta seguro que desea eliminar usuario?');
//      if (result == false){
//           e.preventDefault();
//           this.blur();
//      }
// });