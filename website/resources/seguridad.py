import datetime
import re

from flask import flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash

from website.database import pool_db
from website.models import Users


class Usuario():
    def agregar_usuario(rm,rf):
        if rm == 'POST' and 'name' in rf and 'nick_name' in rf and 'email' in rf and 'phone' in rf and 'ci' in rf and 'city' in rf and 'barrio' in rf and 'nacim' in rf and 'edad' in rf and 'address' in rf and 'password' in rf and 'rol' in rf:
            name = rf['name']
            nick_name = rf['nick_name']
            email = rf['email']
            phone = rf['phone']
            ci = rf['ci']
            city = rf['city']
            barrio = rf['barrio']
            nacim = rf['nacim']
            edad = rf['edad']
            address = rf['address']
            password = rf['password']
            rol = rf['rol']
            _hashed_password = generate_password_hash(password)
            #Comprueba si el nombre de usuario ya existe
            cursor = pool_db.getCursorSgp()
            cursor.execute('SELECT email FROM users WHERE nick_name = %s', (nick_name,))
            account = cursor.fetchone()
            cursor.close()
            # Si el nombre de usuario ya existe, muestra un mensaje
            if account:
                flash('Ya existe esa cuenta!')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('email incorrecto!')
            elif not re.match(r'[A-Za-z0-9]+', nick_name):
                flash('Nombre de usuario solo puede contener letras y/o numeros!')
            elif not nick_name or not password or not email:
                flash('Por favor, complete el formulario!')
            else:
                try:
                    cursor = pool_db.getCursorSgp()
                    # Si la cuenta no existe, se inserta en la base de datos
                    cursor.execute("INSERT INTO users (name, nick_name, email, phone, ci, city, neighborhood, date_birth, age, address, password, rol_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (name, nick_name, email, phone, ci, city, barrio, nacim, edad, address, _hashed_password, rol,))
                    cursor.connection.commit()
                    cursor.close()
                    flash('Registro exitoso!')
                    return redirect(url_for('auth.users'))
                except:
                    flash('No se ha podido completar la operacion')
        elif rm == 'POST':
            # Si el formulario esta vacio...
            flash('Por favor, complete el formulario!')
        return redirect(url_for('auth.users'))
    
    def eliminar_usuario(id):
        user = Users.query.filter_by(id=id).first()
        if user.rol_id == 1:
            flash('Usuario administrador no se puede eliminar')
            return redirect(url_for('auth.users'))
        else:
            try:
                cur = pool_db.getCursorSgp()
                cur.execute('DELETE FROM users WHERE id = {0}'.format(id))
                cur.connection.commit()
                cur.close()
                flash('Usuario eliminado correctamente')
            except:
                flash('No se ha podido completar la operacion') 

    def editar_usuario(rm,rf):
        if rm == 'POST' and 'name' in rf and 'nick_name' in rf and 'email' in rf and 'address' in rf and 'city' in rf and 'phone' in rf and 'barrio' and 'id' in rf and 'rol' in rf:
            name = rf['name']
            nick_name = rf['nick_name']
            email = rf['email']
            phone = rf['phone']
            city = rf['city']
            barrio = rf['barrio']
            address = rf['address']
            id = rf['id']
            rol = rf['rol']
            # cur = pool_db.getCursorSgp()
            # cur.execute('SELECT id, rol_id from users')
            # admin = cur.fetchall()
            # cur.connection.commit()
            # cur.close()
            try:
                cur = pool_db.getCursorSgp()
                cur.execute("UPDATE users SET name=%s, nick_name=%s, email=%s, address=%s, city=%s, phone=%s, neighborhood=%s, rol_id=%s WHERE id = %s", (name, nick_name, email, address, city, phone, barrio, rol, id,))
                cur.connection.commit()
                cur.close()
                flash('Usuario modificado')
            except:
                flash('No se ha podido completar la operacion')

    def asignar_permiso_usuario(rm,rf):
        id_user = rf['edit_id']
        id_permiso = rf['edit_permisos']
        try:
            cur = pool_db.getCursorSgp()
            cur.execute("INSERT INTO user_permisos (id_user, id_permisos) VALUES (%s,%s)",(id_user, id_permiso,))
            cur.connection.commit()
            cur.close()
            flash('Permiso Asignado')
        except Exception as e:
            if hasattr(e, 'message'):
                flash(e.message)
            else:
                flash(e)
            

    def eliminar_permiso_usuario(rm,rf):
        id_user = rf['edit_id']
        id_permiso = rf['edit_permisos']
        try:
            cur = pool_db.getCursorSgp()
            cur.execute('DELETE FROM user_permisos WHERE id_user = {0} and id_permisos = {1}'.format(id_user,id_permiso))
            cur.connection.commit()
            cur.close()
            flash('Permiso eliminado correctamente')
        except Exception as e:
            if hasattr(e, 'message'):
                flash(e.message)
            else:
                flash(e)
class Rol():
    def agregar_rol(rm,rf):
        if rm == 'POST' and 'rol_name' in rf:
            rol_name = rf['rol_name']
            if rol_name == 'Administrador':
                flash('Usuario administrador no se puede agregar')
                return redirect(url_for('auth.roles_permisos'))
            else:
                try:
                    cursor = pool_db.getCursorSgp()
                    #se inserta en la base de datos
                    cursor.execute("INSERT INTO rol (rol_name) VALUES (%s)", (rol_name,))
                    cursor.connection.commit()
                    cursor.close()
                    flash('Rol Creado!')
                    return redirect(url_for('auth.roles_permisos'))
                except:
                    flash('No se ha podido completar la operacion')
        elif rm == 'POST':
            #Si el formulario esta vacio...
            flash('Por favor, complete el formulario!')
        return redirect(url_for('auth.roles_permisos'))

    def eliminar_rol(id):
        if id == 1: ##valida que no se pueda eliminar el administrador
            flash('No se puede eliminar Rol Administrador')
        else:
            try:
                cur = pool_db.getCursorSgp()
                cur.execute('DELETE FROM rol_permisos WHERE id_rol = {0}'.format(id))
                cur.connection.commit()
                cur.close()
                cur = pool_db.getCursorSgp()
                cur.execute('DELETE FROM rol WHERE id = {0}'.format(id))
                cur.connection.commit()
                cur.close()
                flash('Rol eliminado correctamente')
            except:
                flash('No se ha podido completar la operacion')
    
    def editar_rol(rm,rf):
        rol_id = rf['id_rol_edit']
        permiso = rf['rol_permisos_edit']
        try:
            cur = pool_db.getCursorSgp()
            cur.execute("INSERT INTO rol_permisos (id_rol, id_permisos) VALUES (%s,%s)",(rol_id, permiso,))
            cur.connection.commit()
            cur.close()
        except Exception as e:
            if hasattr(e, 'message'):
                flash(e.message)
            else:
                flash(e)

    def asignar_permiso_rol(rm,rf):
        cur = pool_db.getCursorSgp()
        rol = rf['rol_name']
        cur.execute("SELECT id FROM rol WHERE rol_name = %s", (rol,))
        cur.connection.commit()
        id_rol = cur.fetchone()[0]
        cur.close()
        lista_permisos = request.form.getlist('rol_permisos')
        try:
            for permiso in lista_permisos:
                cur = pool_db.getCursorSgp()
                cur.execute("INSERT INTO rol_permisos (id_rol, id_permisos) VALUES (%s,%s)",(id_rol, int(permiso),))
                cur.connection.commit()
                cur.close()
        except Exception as e:
            if hasattr(e, 'message'):
                flash(e.message)
            else:
                flash(e)

    def eliminar_permiso_rol(rm,rf):
        rol_id = rf['id_rol_edit']
        permiso = rf['rol_permisos_edit']
        try:
            cur = pool_db.getCursorSgp()
            cur.execute('DELETE FROM rol_permisos WHERE id_rol = {0} and id_permisos = {1}'.format(rol_id, permiso))
            cur.connection.commit()
            cur.close()
            flash('Permiso eliminado correctamente')
        except Exception as e:
            if hasattr(e, 'message'):
                flash(e.message)
            else:
                flash(e)

            
class Permiso():
    def agregar_permiso(rm,rf):
        if rm == 'POST' and 'permiso_name' in rf:
            if 'es_menu' in rf:
                es_menu = 'yes'
                aux_menu_padre = 0
                id_permiso_name = 1000

            else:
                es_menu = 'no'
                aux_menu_padre = rf['menu_padre']
            permiso_name = rf['permiso_name'] 
            id_permiso_name = rf['id_permiso_name']
            try:
                cursor = pool_db.getCursorSgp()            
                #se inserta en la base de datos
                cursor.execute("INSERT INTO permiso (id,permisos, es_menu, menu_padre) VALUES (%s,%s,%s,%s)", (id_permiso_name,permiso_name, es_menu, aux_menu_padre,))
                cursor.connection.commit()
                cursor.close()
                flash('Permiso Creado!')
                return redirect(url_for('auth.roles_permisos'))
            except:
                flash('No se ha podido completar la operacion')

        elif rm == 'POST':
            #Si el formulario esta vacio...
            flash('Por favor, complete el formulario!')
        return redirect(url_for('auth.roles_permisos'))

    def eliminar_permiso(id):
        try:
            cur = pool_db.getCursorSgp()
            cur.execute('DELETE FROM permiso WHERE id = {0}'.format(id))
            cur.connection.commit()
            cur.close()
            flash('Permiso eliminado correctamente')
        except:
            flash('No se ha podido completar la operacion')

    def editar_permiso(rm,rf):
        if rm == 'POST':
            if 'es_menu' in rf:
                es_menu = 'yes'
                menu_padre = 0
            else:
                es_menu = 'no'
                menu_padre = rf['menu_padre']
            permiso = rf['permiso_name']
            id = rf['id']
        try:
            cur = pool_db.getCursorSgp()
            cur.execute("UPDATE permiso SET permisos=%s, es_menu=%s, menu_padre=%s WHERE id = %s", (permiso, es_menu, menu_padre, id,))
            cur.connection.commit()
            cur.close()
            flash('Usuario modificado')
        except:
            flash('No se ha podido completar la operacion')


class Datos():
    def modificar(rm,rf):
        direccion = rf['address']
        eslogan = rf['eslogan']
        telefono = rf['phone']
        timbrado = rf['timbrado']
        nro_factura = rf['nro-factura']
        factura_inicio = rf['factura-inicio']
        factura_fin = rf['factura-fin']
        email = rf['email']
        ciudad = rf['city']
        barrio = rf['barrio']
        cur = pool_db.getCursorSgp()
        cur.execute("UPDATE empresa SET direccion=%s, eslogan=%s, telefono=%s, timbrado=%s, nro_factura=%s, ciudad=%s, barrio=%s, email=%s, factura_inicio=%s, factura_fin=%s WHERE id = 1",(direccion,eslogan,telefono,timbrado,nro_factura,ciudad,barrio,email,factura_inicio,factura_fin))
        cur.connection.commit()
        cur.close()
        flash('Datos modificados')

        