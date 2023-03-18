$(document).ready(function () {
  $('#reporte_compras').DataTable( {
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


$('.mostrar').on('click', function(){
   $('#mostrar').modal('show');
   var id = $(this).attr('id');
   $.ajax({
     url:"/selectfactura_compra",
     method:"POST",
     data:{id:id},
     success:function(data){
       var data_rs = JSON.parse(data);
       $('#modal-bodyy').html(`
       <table class="table table-striped">
       <thead>
         <tr>
           <th scope="col" class="border-0 text-uppercase font-medium">Orden Compra</th>
           <th scope="col" class="border-0 text-uppercase font-medium">Nro Factura</th>
           <th scope="col" class="border-0 text-uppercase font-medium">Proveedor</th>
           <th scope="col" class="border-0 text-uppercase font-medium">Total</th>
         </tr>
       </thead>
       <tbody>
       <tr>
         <td>${data_rs[0]['id_compra']}</td>
         <td>${data_rs[0]['nro_factura_compra']}</td>
         <td>${data_rs[0]['name']}</td>
         <td>${en_formatter.format(data_rs[0]['monto_total'])} G</td>
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
         var facturaid = data_rs[0]['id_compra'];
         $.ajax({
           url:"/selectdetallefacturacomprareporte",
           method:"POST",
           data:{facturaid:facturaid},
           success:function(data){
             var data_rs2 = JSON.parse(data);
 
             data_rs2.forEach(linea => {
               $('#detalles').append(`
                 <tr>
                   <td>${linea['descripcion']}</td>
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

 $('#imprimir').on('click', function(e){
  $('#imprimir').prop('hidden', true);
  printElement(document.getElementById("PrintThis"));
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