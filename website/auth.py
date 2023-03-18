from flask import (Blueprint, flash, json, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from website.database import pool_db
from website.resources.seguridad import Datos, Permiso, Rol, Usuario

from . import db
from .models import Users

auth = Blueprint('auth', __name__)

# ---------------------------Inicio sistema-----------------------------------------

# Función que permite cargar a una lista los accesos de usuario y de rol
def Access():
    cur = pool_db.getCursorSgp()
    cur.execute("""select p.permisos from permiso p
                    join user_permisos up
                    on p.id = up.id_permisos
                    where id_user = %s""",(current_user.id,))
    access = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute("""select p.permisos from permiso p
                    join rol_permisos rp
                    on p.id = rp.id_permisos
                    where id_rol = %s""",(current_user.rol_id,))
    rol_access = cur.fetchall()
    if rol_access:
        access = access + rol_access
    return access


# Función que genera los datos de la empresa
def Empresa():
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM empresa')
    empresa = cur.fetchone()
    cur.close()
    return empresa

# ---------------------------Login-----------------------------------------

@auth.route('/login', methods=['GET', 'POST'])
def login():
    empresa = Empresa()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user, empresa=empresa)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# ---------------------------Users-----------------------------------------

@auth.route('/users', methods=['GET', 'POST'])
def users():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM rol')
    list_rol = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT id, name, nick_name, neighborhood, age, phone, address, city, email, creation_date, rol_id from users')
    list_users = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute("""WITH RECURSIVE acceso AS (
                    SELECT id, menu_padre, permisos, es_menu, 1 as lvl
                    FROM permiso
                    WHERE menu_padre = 0
                    UNION ALL
                    SELECT p.id, p.menu_padre, p.permisos, p.es_menu, a.lvl+1
                    FROM permiso p
                    JOIN acceso a ON a.id = p.menu_padre )
                SELECT id, menu_padre, permisos, es_menu, lvl FROM acceso;""")
    list_permiso = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute("""select up.id_user, up.id_permisos, p.permisos from user_permisos up
                    join permiso p
                    on p.id = up.id_permisos""")
    list_user_permiso = cur.fetchall()
    cur.close()        
    return render_template('users.html', user=current_user, list_rol=list_rol, list_users=list_users, 
                    list_permiso=list_permiso, list_user_permiso=list_user_permiso, access=access, empresa=empresa)

@auth.route('/agregar_user', methods=['POST', 'GET'])
def agregarUser():
    Usuario.agregar_usuario(request.method,request.form)
    return redirect(url_for('auth.users'))

@auth.route('/editar_user', methods=['POST', 'GET'])
def editarUser():
    Usuario.editar_usuario(request.method,request.form)
    return redirect(url_for('auth.users'))

@auth.route('/eliminar_user/<int:id>', methods=['POST', 'GET'])
def eliminarUser(id):
    Usuario.eliminar_usuario(id)
    return redirect(url_for('auth.users'))

@auth.route('/asignar_permiso_user', methods=['POST', 'GET'])
def asignarPermisoUsuario():
    Usuario.asignar_permiso_usuario(request.method,request.form)
    return redirect(url_for('auth.users'))

@auth.route('/eliminar_permiso_user', methods=['POST', 'GET'])
def eliminarPermisoUsuario():
    Usuario.eliminar_permiso_usuario(request.method,request.form)
    return redirect(url_for('auth.users'))

# Función ajax que permite la carga del modal dinámicamente 
@auth.route('/select', methods=['GET', 'POST'])
def select():   
    if request.method == 'POST': 
        user_id = request.form['user_id']
        print(user_id)      
        cur = pool_db.getCursorSgp()
        result = cur.execute("SELECT * FROM users WHERE id = %s", [user_id])
        rsuser = cur.fetchall()
        cur.close()
        cur = pool_db.getCursorSgp()
        result = cur.execute("SELECT id_permisos FROM user_permisos WHERE id_user = %s", [user_id])
        rsuserpermisos = cur.fetchall()
        cur.close()
        userarray = []
        for rs in rsuser:
            user_dict = {
                    'id': rs['id'],
                    'permisos': rsuserpermisos}
            userarray.append(user_dict)
        return json.dumps(userarray)
        
# ---------------------------------Roles-----------------------------------------

@auth.route('/roles_permisos', methods=['GET', 'POST'])
def roles_permisos():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT id, rol_name from rol')
    list_rol = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute("""WITH RECURSIVE acceso AS (
                    SELECT id,menu_padre, permisos, 1 as lvl
                    FROM permiso
                    WHERE menu_padre = 0
                    UNION ALL
                    SELECT p.id,  p.menu_padre, p.permisos, a.lvl+1
                    FROM permiso p
                    JOIN acceso a ON a.id = p.menu_padre)
                SELECT id,menu_padre, permisos, lvl FROM acceso order by id asc;""")
    list_permiso = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute("""select rp.id_rol, rp.id_permisos, p.permisos from rol_permisos rp
                    join permiso p
                    on p.id = rp.id_permisos""")
    list_rol_permiso = cur.fetchall()
    cur.close()
    return render_template('roles_permisos.html', user=current_user, access=access,
                                list_rol=list_rol, list_permiso=list_permiso, list_rol_permiso=list_rol_permiso, empresa=empresa)

@auth.route('/agregar_rol', methods=['POST', 'GET'])
def agregarRol():
    Rol.agregar_rol(request.method,request.form)
    Rol.asignar_permiso_rol(request.method,request.form)
    return redirect(url_for('auth.roles_permisos'))     

@auth.route('/editar_rol', methods=['POST', 'GET'])
def editarRol():
    Rol.editar_rol(request.method,request.form)
    return redirect(url_for('auth.roles_permisos'))

@auth.route('/eliminar_permiso_rol', methods=['POST', 'GET'])
def eliminarPermisoRol():
    Rol.eliminar_permiso_rol(request.method,request.form)
    return redirect(url_for('auth.roles_permisos'))

@auth.route('/eliminar_rol/<int:id>', methods=['POST', 'GET'])
def eliminarRol(id):
    Rol.eliminar_rol(id)
    return redirect(url_for('auth.roles_permisos'))

# ---------------------------Permisos-----------------------------------------
@auth.route('/agregar_permiso', methods=['POST', 'GET'])
def agregarPermiso():
    Permiso.agregar_permiso(request.method,request.form)
    return redirect(url_for('auth.roles_permisos')) 

@auth.route('/editar_permiso', methods=['POST', 'GET'])
def editarPermiso():
    Permiso.editar_permiso(request.method,request.form)
    return redirect(url_for('auth.roles_permisos'))

@auth.route('/eliminar_permiso/<int:id>', methods=['POST', 'GET'])
def eliminarPermiso(id):
    Permiso.eliminar_permiso(id)
    return redirect(url_for('auth.roles_permisos'))

# ---------------------------Empresa-----------------------------------------
@auth.route('/datos', methods=['POST', 'GET'])
def datos():
    Datos.modificar(request.method,request.form)
    return redirect(url_for('views.home'))

# ---------------------------Debug-----------------------------------------

# Función que permite imprimir en el log con el método {{mdebug()}} en los templates HTML
@auth.context_processor
def utility_functions():
    def print_in_console(message):
        print(message)

    return dict(mdebug=print_in_console)

