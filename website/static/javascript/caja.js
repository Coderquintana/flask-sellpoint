$(document).ready(function(){
    $(document).on('click', '.view_data', function(){
      var nro_caja = $(this).attr("id");
      $.ajax({
        url:"/selectcaja",
        method:"POST",
        data:{nro_caja:nro_caja},
        success:function(data){
          var data_rs = JSON.parse(data);
          if (data_rs[0]['monto_cierre'] != 0){
            alert('Caja Cerrada')
          } else {
            $('#cierre-caja').modal('show');
            $('#nro-caj').val(data_rs[0]['nro_caja']);
            $('#monto-ini').val(data_rs[0]['monto_inicial']);
            $('#user-caja').val(data_rs[0]['user_id']);
            $('#monto-act').val(data_rs[0]['monto_actual']);

          }
        }
      });
    });
    $(document).on('click', '.ver_caja', function(){
      var nro_caja = $(this).attr("id");
      $.ajax({
        url:"/selectcaja",
        method:"POST",
        data:{nro_caja:nro_caja},
        success:function(data){
          var data_rs = JSON.parse(data);
          $('#monto-actual').val(data_rs[0]['monto_actual']);
          $('#monto-inicial').val(data_rs[0]['monto_inicial']);
          $('#cierre').val(data_rs[0]['monto_cierre']);
          new AutoNumeric.multiple('.formato', {
            allowDecimalPadding: false,
            unformatOnSubmit: true,
            decimalCharacter : ',',
            digitGroupSeparator : '.',
          });
        }
      });
    });
}); 

new AutoNumeric.multiple('.formatear', {
  allowDecimalPadding: false,
  unformatOnSubmit: true,
  decimalCharacter : ',',
  digitGroupSeparator : '.',
});