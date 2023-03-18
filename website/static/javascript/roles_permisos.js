$(document).ready(function () {
    $('#tabla_roles').DataTable();
});

$(document).ready(function () {
    $('#tabla_permiso').DataTable();
});

function showAlert(){
    var result = confirm ('Esta seguro que desea eliminar el permiso?');
    if (result == false){
         event.preventDefault();
         btn.blur();
    }
}

// function statusCheck(es_menu) {
//     var menu_padre = document.getElementById("menu_padre");
//     menu_padre.disabled = es_menu.checked ? true : false;
//     if (!menu_padre.disabled) {
//         menu_padre.focus();
//     }
//     menu_padre.value="";
//     menu_padre.placeholder="No tiene Menu Superior";
// }