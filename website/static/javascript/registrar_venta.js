$(document).on('change', '.view_cliente', function(){
  var ci_ruc = $(this).val();
  $.ajax({
    url:"/selectcliente",
    method:"POST",
    data:{ci_ruc:ci_ruc},
    success:function(data){
      var data_rs = JSON.parse(data);
      $('#name').val(data_rs[0]['name']);
      $('#limite').val(data_rs[0]['limite']);
      $('#name').prop('readonly', true);
      $('#ci-ruc').prop('readonly', true);
      $('#producto').focus();
      $(window).scrollTop(350);
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
      $('#ci-ruc').val("");
      $('#limite').val("");
      $('#name').prop('readonly', false)
      $('#ci-ruc').prop('readonly', false);
      $('#modif').prop('hidden',true);
    }
  }
});

var rowIdx = 0;
var p = 0;
var total = 0;
var iva10=0;
var iva5=0;
var bandera = 0;
var valor = 0;

// jQuery button click event to add a row
$('#cantidad').on('change', function () {
  var prod = $('#producto').val();
  var cant = parseInt($('#cantidad').val());
  $('#producto').val('');
  $('#cantidad').val('');
  var aux = '';
  $.ajax({
    url:"/selectproducto",
    method:"POST",
    data:{prod:prod},
    success:function(data){
      var data_rs = JSON.parse(data);
      var precio = data_rs[0]['precio1']

      $('input').each(function(index, value) {
        if (this.value.match(prod) && this.id != 'sgte' && this.name != 'nro-factura'){
          aux = this.id.split('R',-1)[1];
        }
      });
      if (aux != ''){
        total += precio * cant;
        if (data_rs[0]['tipo_impuesto'] === '10%' ){
          iva10 += precio * cant / 11;
        }else if (data_rs[0]['tipo_impuesto'] === '5%'){
          iva5 += precio * cant / 21;
        }
        $('#tabla-total-linea'+aux).html(`<strong>${en_formatter.format(precio * (cant + parseInt($('#cantidadR'+aux).val())))}</strong>`);
        $('#cantidadR'+aux).val(cant + parseInt($('#cantidadR'+aux).val()));
        $('#tabla-cant'+aux).html($('#cantidadR'+aux).val());
        $('#precioR'+aux).html(`<strong>${en_formatter.format(precio)}</strong>`);

      }else{

        
        // Adding a row inside the tbody.
        $('#tbody').append(`
        <tr id="R${++rowIdx}">
          <input class="cantidadR${rowIdx}" type="hidden" value="${cant}" name="cantidadR${rowIdx}" id="cantidadR${rowIdx}">
          <td class="row-index" id="tabla-cant${rowIdx}">
            <strong>${cant}</strong>
          </td>
          <input type="hidden" value="${prod}" name="productoR${rowIdx}" id="productoR${rowIdx}">
          <td class="row-index" id="tabla-prod${rowIdx}">
            <strong>${prod+' - '+data_rs[0]['descripcion']}</strong>
          </td>
          <input type="hidden" value="${precio}" name="precioR${rowIdx}" id="precioR${rowIdx}">
          <input type="hidden" value="${data_rs[0]['tipo_impuesto']}" name="tipo_impuestoR${rowIdx}" id="tipo-impuestoR${rowIdx}">
          <td class="row-index" id="tabla-prec${rowIdx}">
            <strong>${en_formatter.format(precio)}</strong>
          </td>
          <td class="row-index" name="tabla-total-linea" id="tabla-total-linea${rowIdx}">
            <strong>${en_formatter.format(cant * parseInt(precio))}</strong>
          </td>
          <td class="row-index imp-10" hidden>` + (data_rs[0]['tipo_impuesto'] == '10%' ? `${en_formatter.format(precio * cant / 11)}` : `0`) + `
          </td>
          <td class="row-index imp-5" hidden>` + (data_rs[0]['tipo_impuesto'] == '5%' ? `${en_formatter.format(precio * cant / 21)}` : `0`) + `
          </td>
          <td class="text-center">
            <button class="btn btn-danger btn-sm remove" id="btnR${rowIdx}" type="button" hidden><i class="bi bi-x-circle"></i></button>
          </td>
        </tr>`);
        total += cant * parseInt(precio);
        if (data_rs[0]['tipo_impuesto'] === '10%' ){
          iva10 += precio * cant / 11;
        }else if (data_rs[0]['tipo_impuesto'] === '5%'){
          iva5 += precio * cant / 21;
        }
      }
      $('#total').text(en_formatter.format(total));
      $('#total2').html("TOTAL: " + en_formatter.format(total));
      $('#iva10').text(en_formatter.format(iva10));
      $('#iva5').text(en_formatter.format(iva5));
      $('#sub-total').text(en_formatter.format(total-iva10-iva5));
      $('#monto-total').val(total);
      $('#num-letra').html(NumeroALetras(total));
    }
  });
});

jQuery("#text-1").on("click", function() {
  bootbox.prompt({
      title: "What's your name", 
      inputType: "text",
      callback: function(result) {
          showResult(result);
      }
  });
});

$('#mod-detalle').on('click', function () {
  $('#verificar').modal("show");
});

$('#validar').on('click',function(){
  var Val = $('#contraseña').val();
  
  if (Val != 'admin'){
    alert("Contraseña no válida!")
    e.preventDefault();
  }else{
    $('#verificar').modal('hide');
    $('.remove').attr('hidden',false);
    $('#mod-detalle').attr('hidden',true);
    $('#listo').attr('hidden',false);
  }
});

$('#listo').on('click', function(){
  $('#listo').attr('hidden',true);
  $('#mod-detalle').attr('hidden', false);
  $('.remove').attr('hidden',true);
});

// jQuery button click event to remove a row.
$('#tbody').on('click', '.remove', function (e) {
  // Getting all the rows next to the row
  // containing the clicked button
  var child = $(this).closest('tr').nextAll();    
  var x = aux = this.id.split('R',-1)[1];
  var linea = $(this).closest('tr').find('#tabla-total-linea'+x).text().replace(/[^\d\,\-]/g, "");
  var preciolinea = $(this).closest('tr').find('#precioR'+x).val();
  var cantidadlinea = parseInt($(this).closest('tr').find('#cantidadR'+x).val());
  var impuesto = $(this).closest('tr').find('#tipo-impuestoR'+x).val();
  

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

  $('#total').text(en_formatter.format(total-linea));
  $('#total2').text("TOTAL: " + en_formatter.format(total-linea));
  total = total - linea;
  $('#monto-total').val(parseInt($('#monto-total').val())-linea);
  
  if (impuesto === '10%' ){
    iva10 -= preciolinea * cantidadlinea / 11;
  }else if (impuesto === '5%'){
    iva5 -= preciolinea * cantidadlinea / 21;
  }
  $('#iva10').text(en_formatter.format(iva10));
  $('#iva5').text(en_formatter.format(iva5));
  $('#sub-total').text(en_formatter.format(total-iva10-iva5))
});

$('#deli').on('change', function(){
  if ($('#deli').is(':checked')){
    $('#delivery-ci').prop('hidden', false);
    $('#delivery-phone').prop('hidden', false);

    $('#l-deli1').prop('hidden', false);
    $('#l-deli2').prop('hidden', false);
  }else{
    $('#delivery-ci').prop('hidden', true);
    $('#delivery-phone').prop('hidden', true);

    $('#l-deli1').prop('hidden', true);
    $('#l-deli2').prop('hidden', true);
  }
});

$('#carga-pedido').on('click', function(){
  var pedido = $('#pedido').val();
  $('#es-pedido').val('1');
  $('#pedido-id').val(pedido);
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
            $('#sgte-pedido').val(pedido);
            $('#name').prop('readonly', true);
            $('#ci-ruc').prop('readonly', true);
            $('#producto').prop('readonly', true);
            $('#cantidad').prop('readonly', true);
            $('#cancelar').prop('hidden', false);
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
                  <input type="hidden" value="${linea['cantidad']}" name="cantidadR${rowIdx}" id="cantidadR${rowIdx}">
                  <td class="row-index" id="tabla-cant${rowIdx}">
                    ${linea['cantidad']}
                  </td>
                  <input type="hidden" value="${linea['codigo']}" name="productoR${rowIdx}" id="productoR${rowIdx}">
                  <td class="row-index" id="tabla-prod${rowIdx}">
                    ${linea['codigo']}
                  </td>
                  <input type="hidden" value="${linea['precio']}" name="precioR${rowIdx}">
                  <td class="row-index" id="tabla-prec${rowIdx}">
                    ${en_formatter.format(linea['precio'])}
                  </td>
                  <td class="row-index" name="tabla-total-linea" id="tabla-total-linea${rowIdx}">
                    ${en_formatter.format(linea['cantidad']*linea['precio'])}
                  </td>
                  <td class="text-center">
                    <button class="btn btn-danger btn-sm remove" id="btnR${rowIdx}" type="button" hidden><i class="bi bi-x-circle"></i></button>
                  </td>
                </tr>`);
                if (linea['tipo_impuesto'] === '10%' ){
                  iva10 += linea['precio'] * linea['cantidad'] / 11;
                }else if (linea['tipo_impuesto'] === '5%'){
                  iva5 += linea['precio'] * linea['cantidad'] / 21;
                }
                total += linea['cantidad']*linea['precio'];
                $('#total').text(en_formatter.format(total));
                $('#iva10').text(en_formatter.format(iva10));
                $('#iva5').text(en_formatter.format(iva5));
                $('#sub-total').text(en_formatter.format(total-iva10-iva5))
                $('#monto-total').val(total);
                $('#num-letra').html(NumeroALetras(total));
            });
          }
        });               
    }
  });
});

$('#cancelar').on('click', function(){
  location.reload();
});

$(document).ready(function(){
  var nro_factura = $('#sgte').val();
  var timbrado = $('#timbr').val();
  $('#nro-factura').html("Factura Nro: " + nro_factura);
  $('#timbrado').html("Timbrado: " + timbrado);
  $('#user').html("Usuario Actual: " + $('#user-id').val());
  $('#ci-ruc').focus();
  new AutoNumeric.multiple('.formato', {
    allowDecimalPadding: false,
    unformatOnSubmit: true,
    decimalCharacter : '.',
    digitGroupSeparator : ',',
  });
});


$('#confirmar').on('click', function(e){
  if ($('#ci-ruc').val() == ''){
    alert("Seleccione Cliente")
    $('#ci-ruc').focus();
    $(window).scrollTop(top);
    e.preventDefault();
  }
  if ($('#cantidadR1').length) {
    $('#pago').modal('show');
  } else {
    alert("Factura sin detalle")
    e.preventDefault();
    $('#producto').focus();
  }
});

$('#pago').on('shown.bs.modal', function () {
  $('#recibido').val($('#monto-total').val());
  
  $('#cobro').html("Cobrar: " + en_formatter.format($('#monto-total').val()));
  $('#recibido').focus();
  $('#vuelto').text('0');
  $('#recibido').select();
});

$('modal').on('data-bs-dismiss', function (e) {
  e.preventDefault();
  $(window).scrollTop(top);
});

$('#recibido').on('keyup', function(){
  var calculo = parseInt($('#recibido').val().replace(/[^\d\.\-]/g, ""))-parseInt($('#monto-total').val().replace(/[^\d\.\-]/g, ""))
  $('#diferencia').val(en_formatter.format(calculo));
});

$('#credito').on('change click',function(){
  $('#efectivo').prop('disabled', true);
  $('#tarjeta').prop('disabled', true);
  $('#transferencia').prop('disabled', true);
  $('#recibido').prop('readonly', true);
  $('#recibido').val(en_formatter.format($('#limite').val()));
  $('#diferencia').val(en_formatter.format(parseInt($('#recibido').val().replace(/[^\d\,\-]/g, ""))-parseInt($('#monto-total').val())));
  $('#recib').html("Credito Disponible:");
  $('#pago-titulo').html("Gestionar Pago  ---->     CREDITO DISPONIBLE: " + en_formatter.format($('#limite').val()));
  $('#vuelt').prop('hidden',true);
  $('#diferencia').prop('hidden',true);
  $('#credit').prop("checked", true);
});

$('#contado').on('change click',function(){
  $('#efectivo').prop('disabled', false);
  $('#tarjeta').prop('disabled', false);
  $('#transferencia').prop('disabled', false);
  $('#recibido').prop('readonly', false);
  $('#recib').html("Recibido:");
  $('#pago-titulo').html("Gestionar Pago");
  $('#recibido').val(en_formatter.format($('#monto-total').val()));
  $('#diferencia').val(parseInt($('#recibido').val().replace(/[^\d\,\-]/g, ""))-parseInt($('#monto-total').val()));
  $('#contad').prop("checked", true);
  $('#vuelt').prop('hidden',false);
  $('#diferencia').prop('hidden',false);
});

$('#efectivo').on('change click' ,function(){
  $('#tarje').prop('hidden',true);
  $('#tarj').prop('hidden', true);
  $('#nro-cuenta').prop('hidden',true);
  $('#nro-cuen').prop('hidden',true);
  $('#recib').prop('hidden',false);
  $('#recibido').prop('hidden',false);
  $('#diferencia').prop('hidden',false);
  $('#vuelt').prop('hidden',false);
  $('#recibido').val('');
  $('#diferencia').val('');
});

$('#tarjeta').on('change click' ,function(){
  $('#recib').prop('hidden',true);
  $('#recibido').prop('hidden',true);
  $('#diferencia').prop('hidden',true);
  $('#vuelt').prop('hidden',true);
  $('#nro-cuenta').prop('hidden',true);
  $('#nro-cuen').prop('hidden',true);
  $('#tarje').prop('hidden',false);
  $('#tarj').prop('hidden', false);
});

$('#transferencia').on('change click' ,function(){
  $('#recib').prop('hidden',true);
  $('#recibido').prop('hidden',true);
  $('#diferencia').prop('hidden',true);
  $('#vuelt').prop('hidden',true);
  $('#tarje').prop('hidden',true);
  $('#tarj').prop('hidden', true);
  $('#nro-cuenta').prop('hidden',false);
  $('#nro-cuent').prop('hidden',false);
  $('#recibido').val('');
  $('#diferencia').val('');
});

$('#form').on('keypress', function(e) {
  var keyCode = e.keyCode || e.which;
  if (keyCode === 13) { 
    e.preventDefault();
    $('#confirmar').click();
    return false;
  }
});

$('#guardar').on('click', function(e){
  if (parseInt($('#diferencia').val()) < 0 && $('#credito').prop('cheched', true)){
    alert('A superado su límite de crédito');
    e.preventDefault();
    return false;
  }else{
    $('#pago').modal('hide');
    $('#user').html('Desde: 01-01-2022 Hasta: 31-12-2022');
    $('#condi-pago').prop('hidden',false);
    document.title = $('#sgte').val();
    $('.imp-10').prop('hidden', false);
    $('.imp-5').prop('hidden', false);
    $('#num-letra').prop('hidden', false);
    $('#num-letras').prop('hidden', false);
    printElement(document.getElementById("printThis"));
  }
});

$('#volver').on('click', function(){
  $('#contado').click();
});

$('#recibido').on('keypress', function(e){
  var keyCode = e.keyCode || e.which;
  if (keyCode === 13) { 
    $('#guardar').click();
  }
});

$(document).on("focusout","#cantidad",function(){
  $('#cantidad').change();
});

const en_formatter = new Intl.NumberFormat('es-ES', {maximumFractionDigits: 0 });
//  style: 'currency', currency: 'PYG'
var bander = 0;
$(document).ready(function(){

  var scanner = new Instascan.Scanner({ video: document.getElementById('preview'), scanPeriod: 5, mirror: false });
  scanner.addListener('scan',function(content){
      if (bander>0){
        $('#cantidad').change();
        bander+=1;
      }else{
        bander=1;
      }
      $('#producto').val(content);
      $('#cantidad').val('1');
      $('#cantidad').focus();

      beep();

      //window.location.href=content;
  });
  Instascan.Camera.getCameras().then(function (cameras){
      if(cameras.length>0){
          scanner.start(cameras[0]);
          $('[name="options"]').on('change',function(){
              if($(this).val()==1){
                  if(cameras[0]!=""){
                      scanner.start(cameras[0]);
                  }else{
                      alert('No Front camera found!');
                  }
              }else if($(this).val()==2){
                  if(cameras[1]!=""){
                      scanner.start(cameras[1]);
                  }else{
                      alert('No Back camera found!');
                  }
              }
          });
      }else{
          console.error('No cameras found.');
          alert('No cameras found.');
      }
  }).catch(function(e){
      console.error(e);
      alert(e);
  });
  $('#terminar').on('click',function(){
    scanner.stop();
    $('#preview').prop('hidden', false);
  });
});

$('.myselect').select2({
  placeholder: "Filtrar",
  allowClear: true,
  dropdownParent: $("#modal-pedido")
});

function beep() {
  var snd = new Audio("data:audio/wav;base64,//uQRAAAAWMSLwUIYAAsYkXgoQwAEaYLWfkWgAI0wWs/ItAAAGDgYtAgAyN+QWaAAihwMWm4G8QQRDiMcCBcH3Cc+CDv/7xA4Tvh9Rz/y8QADBwMWgQAZG/ILNAARQ4GLTcDeIIIhxGOBAuD7hOfBB3/94gcJ3w+o5/5eIAIAAAVwWgQAVQ2ORaIQwEMAJiDg95G4nQL7mQVWI6GwRcfsZAcsKkJvxgxEjzFUgfHoSQ9Qq7KNwqHwuB13MA4a1q/DmBrHgPcmjiGoh//EwC5nGPEmS4RcfkVKOhJf+WOgoxJclFz3kgn//dBA+ya1GhurNn8zb//9NNutNuhz31f////9vt///z+IdAEAAAK4LQIAKobHItEIYCGAExBwe8jcToF9zIKrEdDYIuP2MgOWFSE34wYiR5iqQPj0JIeoVdlG4VD4XA67mAcNa1fhzA1jwHuTRxDUQ//iYBczjHiTJcIuPyKlHQkv/LHQUYkuSi57yQT//uggfZNajQ3Vmz+Zt//+mm3Wm3Q576v////+32///5/EOgAAADVghQAAAAA//uQZAUAB1WI0PZugAAAAAoQwAAAEk3nRd2qAAAAACiDgAAAAAAABCqEEQRLCgwpBGMlJkIz8jKhGvj4k6jzRnqasNKIeoh5gI7BJaC1A1AoNBjJgbyApVS4IDlZgDU5WUAxEKDNmmALHzZp0Fkz1FMTmGFl1FMEyodIavcCAUHDWrKAIA4aa2oCgILEBupZgHvAhEBcZ6joQBxS76AgccrFlczBvKLC0QI2cBoCFvfTDAo7eoOQInqDPBtvrDEZBNYN5xwNwxQRfw8ZQ5wQVLvO8OYU+mHvFLlDh05Mdg7BT6YrRPpCBznMB2r//xKJjyyOh+cImr2/4doscwD6neZjuZR4AgAABYAAAABy1xcdQtxYBYYZdifkUDgzzXaXn98Z0oi9ILU5mBjFANmRwlVJ3/6jYDAmxaiDG3/6xjQQCCKkRb/6kg/wW+kSJ5//rLobkLSiKmqP/0ikJuDaSaSf/6JiLYLEYnW/+kXg1WRVJL/9EmQ1YZIsv/6Qzwy5qk7/+tEU0nkls3/zIUMPKNX/6yZLf+kFgAfgGyLFAUwY//uQZAUABcd5UiNPVXAAAApAAAAAE0VZQKw9ISAAACgAAAAAVQIygIElVrFkBS+Jhi+EAuu+lKAkYUEIsmEAEoMeDmCETMvfSHTGkF5RWH7kz/ESHWPAq/kcCRhqBtMdokPdM7vil7RG98A2sc7zO6ZvTdM7pmOUAZTnJW+NXxqmd41dqJ6mLTXxrPpnV8avaIf5SvL7pndPvPpndJR9Kuu8fePvuiuhorgWjp7Mf/PRjxcFCPDkW31srioCExivv9lcwKEaHsf/7ow2Fl1T/9RkXgEhYElAoCLFtMArxwivDJJ+bR1HTKJdlEoTELCIqgEwVGSQ+hIm0NbK8WXcTEI0UPoa2NbG4y2K00JEWbZavJXkYaqo9CRHS55FcZTjKEk3NKoCYUnSQ0rWxrZbFKbKIhOKPZe1cJKzZSaQrIyULHDZmV5K4xySsDRKWOruanGtjLJXFEmwaIbDLX0hIPBUQPVFVkQkDoUNfSoDgQGKPekoxeGzA4DUvnn4bxzcZrtJyipKfPNy5w+9lnXwgqsiyHNeSVpemw4bWb9psYeq//uQZBoABQt4yMVxYAIAAAkQoAAAHvYpL5m6AAgAACXDAAAAD59jblTirQe9upFsmZbpMudy7Lz1X1DYsxOOSWpfPqNX2WqktK0DMvuGwlbNj44TleLPQ+Gsfb+GOWOKJoIrWb3cIMeeON6lz2umTqMXV8Mj30yWPpjoSa9ujK8SyeJP5y5mOW1D6hvLepeveEAEDo0mgCRClOEgANv3B9a6fikgUSu/DmAMATrGx7nng5p5iimPNZsfQLYB2sDLIkzRKZOHGAaUyDcpFBSLG9MCQALgAIgQs2YunOszLSAyQYPVC2YdGGeHD2dTdJk1pAHGAWDjnkcLKFymS3RQZTInzySoBwMG0QueC3gMsCEYxUqlrcxK6k1LQQcsmyYeQPdC2YfuGPASCBkcVMQQqpVJshui1tkXQJQV0OXGAZMXSOEEBRirXbVRQW7ugq7IM7rPWSZyDlM3IuNEkxzCOJ0ny2ThNkyRai1b6ev//3dzNGzNb//4uAvHT5sURcZCFcuKLhOFs8mLAAEAt4UWAAIABAAAAAB4qbHo0tIjVkUU//uQZAwABfSFz3ZqQAAAAAngwAAAE1HjMp2qAAAAACZDgAAAD5UkTE1UgZEUExqYynN1qZvqIOREEFmBcJQkwdxiFtw0qEOkGYfRDifBui9MQg4QAHAqWtAWHoCxu1Yf4VfWLPIM2mHDFsbQEVGwyqQoQcwnfHeIkNt9YnkiaS1oizycqJrx4KOQjahZxWbcZgztj2c49nKmkId44S71j0c8eV9yDK6uPRzx5X18eDvjvQ6yKo9ZSS6l//8elePK/Lf//IInrOF/FvDoADYAGBMGb7FtErm5MXMlmPAJQVgWta7Zx2go+8xJ0UiCb8LHHdftWyLJE0QIAIsI+UbXu67dZMjmgDGCGl1H+vpF4NSDckSIkk7Vd+sxEhBQMRU8j/12UIRhzSaUdQ+rQU5kGeFxm+hb1oh6pWWmv3uvmReDl0UnvtapVaIzo1jZbf/pD6ElLqSX+rUmOQNpJFa/r+sa4e/pBlAABoAAAAA3CUgShLdGIxsY7AUABPRrgCABdDuQ5GC7DqPQCgbbJUAoRSUj+NIEig0YfyWUho1VBBBA//uQZB4ABZx5zfMakeAAAAmwAAAAF5F3P0w9GtAAACfAAAAAwLhMDmAYWMgVEG1U0FIGCBgXBXAtfMH10000EEEEEECUBYln03TTTdNBDZopopYvrTTdNa325mImNg3TTPV9q3pmY0xoO6bv3r00y+IDGid/9aaaZTGMuj9mpu9Mpio1dXrr5HERTZSmqU36A3CumzN/9Robv/Xx4v9ijkSRSNLQhAWumap82WRSBUqXStV/YcS+XVLnSS+WLDroqArFkMEsAS+eWmrUzrO0oEmE40RlMZ5+ODIkAyKAGUwZ3mVKmcamcJnMW26MRPgUw6j+LkhyHGVGYjSUUKNpuJUQoOIAyDvEyG8S5yfK6dhZc0Tx1KI/gviKL6qvvFs1+bWtaz58uUNnryq6kt5RzOCkPWlVqVX2a/EEBUdU1KrXLf40GoiiFXK///qpoiDXrOgqDR38JB0bw7SoL+ZB9o1RCkQjQ2CBYZKd/+VJxZRRZlqSkKiws0WFxUyCwsKiMy7hUVFhIaCrNQsKkTIsLivwKKigsj8XYlwt/WKi2N4d//uQRCSAAjURNIHpMZBGYiaQPSYyAAABLAAAAAAAACWAAAAApUF/Mg+0aohSIRobBAsMlO//Kk4soosy1JSFRYWaLC4qZBYWFRGZdwqKiwkNBVmoWFSJkWFxX4FFRQWR+LsS4W/rFRb/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////VEFHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAU291bmRib3kuZGUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMjAwNGh0dHA6Ly93d3cuc291bmRib3kuZGUAAAAAAAAAACU=");  
  snd.play();
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
}



function Unidades(num){

      switch(num)
      {
          case 1: return "UN";
          case 2: return "DOS";
          case 3: return "TRES";
          case 4: return "CUATRO";
          case 5: return "CINCO";
          case 6: return "SEIS";
          case 7: return "SIETE";
          case 8: return "OCHO";
          case 9: return "NUEVE";
      }

      return "";
      }//Unidades()

      function Decenas(num){

      decena = Math.floor(num/10);
      unidad = num - (decena * 10);

      switch(decena)
      {
          case 1:
              switch(unidad)
              {
                  case 0: return "DIEZ";
                  case 1: return "ONCE";
                  case 2: return "DOCE";
                  case 3: return "TRECE";
                  case 4: return "CATORCE";
                  case 5: return "QUINCE";
                  default: return "DIECI" + Unidades(unidad);
              }
          case 2:
              switch(unidad)
              {
                  case 0: return "VEINTE";
                  default: return "VEINTI" + Unidades(unidad);
              }
          case 3: return DecenasY("TREINTA", unidad);
          case 4: return DecenasY("CUARENTA", unidad);
          case 5: return DecenasY("CINCUENTA", unidad);
          case 6: return DecenasY("SESENTA", unidad);
          case 7: return DecenasY("SETENTA", unidad);
          case 8: return DecenasY("OCHENTA", unidad);
          case 9: return DecenasY("NOVENTA", unidad);
          case 0: return Unidades(unidad);
      }
      }//Unidades()

      function DecenasY(strSin, numUnidades) {
      if (numUnidades > 0)
      return strSin + " Y " + Unidades(numUnidades)

      return strSin;
      }//DecenasY()

      function Centenas(num) {
      centenas = Math.floor(num / 100);
      decenas = num - (centenas * 100);

      switch(centenas)
      {
          case 1:
              if (decenas > 0)
                  return "CIENTO " + Decenas(decenas);
              return "CIEN";
          case 2: return "DOSCIENTOS " + Decenas(decenas);
          case 3: return "TRESCIENTOS " + Decenas(decenas);
          case 4: return "CUATROCIENTOS " + Decenas(decenas);
          case 5: return "QUINIENTOS " + Decenas(decenas);
          case 6: return "SEISCIENTOS " + Decenas(decenas);
          case 7: return "SETECIENTOS " + Decenas(decenas);
          case 8: return "OCHOCIENTOS " + Decenas(decenas);
          case 9: return "NOVECIENTOS " + Decenas(decenas);
      }

      return Decenas(decenas);
      }//Centenas()

      function Seccion(num, divisor, strSingular, strPlural) {
      cientos = Math.floor(num / divisor)
      resto = num - (cientos * divisor)

      letras = "";

      if (cientos > 0)
          if (cientos > 1)
              letras = Centenas(cientos) + " " + strPlural;
          else
              letras = strSingular;

      if (resto > 0)
          letras += "";

      return letras;
      }//Seccion()

      function Miles(num) {
      divisor = 1000;
      cientos = Math.floor(num / divisor)
      resto = num - (cientos * divisor)

      strMiles = Seccion(num, divisor, "UN MIL", "MIL");
      strCentenas = Centenas(resto);

      if(strMiles == "")
          return strCentenas;

      return strMiles + " " + strCentenas;
      }//Miles()

      function Millones(num) {
      divisor = 1000000;
      cientos = Math.floor(num / divisor)
      resto = num - (cientos * divisor)

      strMillones = Seccion(num, divisor, "UN MILLON DE", "MILLONES DE");
      strMiles = Miles(resto);

      if(strMillones == "")
          return strMiles;

      return strMillones + " " + strMiles;
      }//Millones()

      function NumeroALetras(num) {
      var data = {
          numero: num,
          enteros: Math.floor(num),
          centavos: (((Math.round(num * 100)) - (Math.floor(num) * 100))),
          letrasCentavos: "",
          letrasMonedaPlural: 'Guaraníes',//"PESOS", 'Dólares', 'Bolívares', 'etcs'
          letrasMonedaSingular: 'Guaraní', //"PESO", 'Dólar', 'Bolivar', 'etc'

          letrasMonedaCentavoPlural: "CENTAVOS",
          letrasMonedaCentavoSingular: "CENTAVO"
      };

      if (data.centavos > 0) {
          data.letrasCentavos = "CON " + (function (){
              if (data.centavos == 1)
                  return Millones(data.centavos) + " " + data.letrasMonedaCentavoSingular;
              else
                  return Millones(data.centavos) + " " + data.letrasMonedaCentavoPlural;
              })();
      };

      if(data.enteros == 0)
          return "CERO " + data.letrasMonedaPlural + " " + data.letrasCentavos;
      if (data.enteros == 1)
          return Millones(data.enteros) + " " + data.letrasMonedaSingular + " " + data.letrasCentavos;
      else
          return Millones(data.enteros) + " " + data.letrasMonedaPlural + " " + data.letrasCentavos;
      }