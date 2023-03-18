var monto_fac = 0;
$(document).on('change', '.view_cliente2', function(){
  var ci_ruc = $(this).val();
  $.ajax({
    url:"/selectcliente2",
    method:"POST",
    data:{ci_ruc:ci_ruc},
    success:function(data){
      var data_rs = JSON.parse(data);
      $('#name').val(data_rs[0]['name'])
    }
  });

  $.ajax({
    url:"/selectfactura2",
    method:"POST",
    data:{ci_ruc:ci_ruc},
    success:function(data){
      var data_rs = JSON.parse(data);
      data_rs.forEach(linea => {
        $('#factura').append(`
          <option value="${linea['nro_factura']}">${linea['nro_factura']} </option>;
          
          `);

      });
    }
  });
});

$('#efectivo').on('change', function(){
  if ($('#efectivo').is(':checked')){
    $('#total_cobro_efe').val(monto_fac);
    $('#dato_tar').prop('hidden', true);
    $('#lbl_tar').prop('hidden', true);
    $('#total_cobro_tar').val("");

    $('#dato_tra').prop('hidden', true);
    $('#lbl_tra').prop('hidden', true);
    $('#total_cobro_tra').val("");
  }
});
$('#tarjeta').on('change', function(){
  if ($('#tarjeta').is(':checked')){
    $('#dato_tar').prop('hidden', false);
    $('#lbl_tar').prop('hidden', false);
    $('#total_cobro_tar').val($('#total_cobro_efe').val());
    $('#total_cobro_efe').val("");

    $('#dato_tra').prop('hidden', true);
    $('#lbl_tra').prop('hidden', true);
    $('#total_cobro_tra').val("");
  }else{
    $('#dato_tar').prop('hidden', true);
    $('#lbl_tar').prop('hidden', true);
    $('#total_cobro_tar').val("");
    $('#total_cobro_efe').val(monto_fac);
  }
});
  $('#transferencia').on('change', function(){
  if ($('#transferencia').is(':checked')){
    $('#dato_tra').prop('hidden', false);
    $('#lbl_tra').prop('hidden', false);
    $('#total_cobro_tra').val($('#total_cobro_efe').val());
    $('#total_cobro_efe').val("");

    $('#dato_tar').prop('hidden', true);
    $('#lbl_tar').prop('hidden', true);
    $('#total_cobro_tar').val("");
  }else{
    $('#dato_tra').prop('hidden', true);
    $('#lbl_tra').prop('hidden', true);
    $('#total_cobro_tra').val("");
    $('#total_cobro_efe').val(monto_fac);
  }
});

$('#factura').on('change', function(){
    var ci_ruc = $('#ci-ruc').val();
    $.ajax({
      url:"/selectfactura2",
      method:"POST",
      data:{ci_ruc:ci_ruc},
      success:function(data){
        var data_rs = JSON.parse(data);
            $('#total_cobro_efe').val(data_rs[0]['monto']);
      }
    });
  
});

$('#guardar').on('click', function(){
    printElement(document.getElementById("printThis"));
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
 