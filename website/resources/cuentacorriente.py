import email
from website.database import pool_db
import datetime
from werkzeug.security import generate_password_hash
from flask import render_template, flash, redirect, url_for
import re 
from website.models import clientes, proveedores

class Cliente():
    def agregar_cliente(rm,rf):
        if rm == 'POST' and 'tipo_documento' in rf and 'ci_ruc' in rf and 'name' in rf and 'address' in rf and 'email' in rf and 'phone' in rf and 'city' in rf and 'neighborhood'in rf and 'cred_limite' in rf and 'estado' in rf:
            tipo_documento = rf['tipo_documento']
            ci_ruc = rf['ci_ruc']
            name = rf['name']
            address = rf['address']
            email = rf['email']
            phone = rf['phone']
            city = rf['city']
            neighborhood = rf['neighborhood']
            cred_limite = rf['cred_limite']
            estado = rf['estado']
            #Comprueba si el numero de documento ya existe
            cursor = pool_db.getCursorSgp()
            cursor.execute('SELECT ci_ruc FROM clientes WHERE ci_ruc = %s', (ci_ruc,))
            account = cursor.fetchone()
            cursor.close()
            # Si el nombre de usuario ya existe, muestra un mensaje
            if account:
                flash('Ya existe esa cuenta!')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Email incorrecto!')
            elif not ci_ruc or not name or not tipo_documento:
                flash('Por favor, complete el formulario!')
            else:
                cursor = pool_db.getCursorSgp()
                # Si el cliente no existe, se inserta en la base de datos
                cursor.execute("INSERT INTO clientes (tipo_documento, ci_ruc, name, address, email, phone, city, cred_limite, neighborhood, estado) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (tipo_documento, ci_ruc, name, address, email, phone, city, cred_limite, neighborhood, estado,))
                cursor.connection.commit()
                cursor.close()
                flash('Registro exitoso!')
                return redirect(url_for('views.clientes'))
        elif rm == 'POST':
            # Si el formulario esta vacio...
            flash('Por favor, complete el formulario!')
        return redirect(url_for('views.clientes'))

    def editar_cliente(rm,rf):
        if rm == 'POST' and 'tipo_documento' in rf and 'ci_ruc' in rf and 'name' in rf and 'address' in rf and 'email' in rf and 'phone' in rf and 'city' in rf and 'neighborhood'in rf and 'cred_limite' in rf and 'estado' in rf and 'id' in rf:
            tipo_documento = rf['tipo_documento']
            id = rf['id']
            ci_ruc = rf['ci_ruc']
            name = rf['name']
            address = rf['address']
            email = rf['email']
            phone = rf['phone']
            city = rf['city']
            neighborhood = rf['neighborhood']
            cred_limite = rf['cred_limite']
            estado = rf['estado']
            #Comprueba si el numero de documento ya existe
            cursor = pool_db.getCursorSgp()
            cursor.execute("UPDATE clientes SET tipo_documento=%s, ci_ruc=%s, name=%s, address=%s, email=%s, phone=%s, city=%s, neighborhood=%s, cred_limite=%s, estado=%s WHERE id = %s", (tipo_documento, ci_ruc, name, address, email, phone, city, neighborhood, cred_limite, estado, id,))
            cursor.connection.commit()
            cursor.close()
            flash('Cliente Modificado!')

class Proveedor():
    def agregar_proveedor(rm,rf):
        if rm == 'POST' and 'tipo_documento' in rf and 'ci_ruc' in rf and 'name' in rf and 'address' in rf and 'phone' in rf and 'email' in rf and 'city' in rf and 'neighborhood' in rf:
            tipo_documento = rf['tipo_documento']
            ci_ruc = rf['ci_ruc']
            name = rf['name']
            address = rf['address']
            email = rf['email']
            phone = rf['phone']
            city = rf['city']
            neighborhood = rf['neighborhood']
            #Comprueba si el numero de documento ya existe
            cursor = pool_db.getCursorSgp()
            cursor.execute('SELECT ci_ruc FROM proveedores WHERE ci_ruc = %s', (ci_ruc,))
            account = cursor.fetchone()
            cursor.close()
            # Si el nombre de usuario ya existe, muestra un mensaje
            if account:
                flash('Ya existe esa cuenta!')
            elif not ci_ruc or not name or not tipo_documento:
                flash('Por favor, complete el formulario!')
            else:
                cursor = pool_db.getCursorSgp()
                # Si el cliente no existe, se inserta en la base de datos
                cursor.execute("INSERT INTO proveedores (tipo_documento, ci_ruc, name, address, email, phone, city, neighborhood) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (tipo_documento, ci_ruc, name, address, email, phone, city, neighborhood,))
                cursor.connection.commit()
                cursor.close()
                flash('Registro exitoso!')
                return redirect(url_for('views.proveedores'))
        elif rm == 'POST':
            # Si el formulario esta vacio...
            flash('Por favor, complete el formulario!')
        return redirect(url_for('views.proveedores'))

    def editar_proveedor(rm,rf):
        if rm == 'POST' and 'tipo_documento' in rf and 'ci_ruc' in rf and 'name' in rf and 'address' in rf and 'email' in rf and 'phone' in rf and 'city' in rf and 'neighborhood' in rf:
            tipo_documento = rf['tipo_documento']
            id = rf['id']
            ci_ruc = rf['ci_ruc']
            name = rf['name']
            address = rf['address']
            email = rf['email']
            phone = rf['phone']
            city = rf['city']
            neighborhood = rf['neighborhood']
            #Comprueba si el numero de documento ya existe
            cursor = pool_db.getCursorSgp()
            cursor.execute("UPDATE proveedores SET tipo_documento=%s, ci_ruc=%s, name=%s, address=%s, email=%s, phone=%s, city=%s, neighborhood=%s WHERE id = %s", (tipo_documento, ci_ruc, name, address, email, phone, city, neighborhood, id, ))
            cursor.connection.commit()
            cursor.close()
            flash('Proveedor Modificado')

class Cobros:
    def agregar_cobro(rm,rf):
        if rm == 'POST' and 'nro_recibo' in rf:
            nro_recibo = rf['nro_recibo']
            ci_ruc = rf['ci-ruc']
            nombre = rf['name']
            total_efectivo = rf['total_cobro_efe']
            total_transferencia = rf['total_cobro_tra']
            total_tarjeta = rf['total_cobro_tar']
            descripcion = rf['descripcion']
            factura = rf['factura']
            tipo_cobro = rf['tipo_pago']

            if tipo_cobro == 'Tarjeta':
                dato_tar = rf['dato_tar']
                total_cobrado = total_tarjeta
                total_efectivo = 0
                total_transferencia = 0
            elif tipo_cobro == 'Transferencia':
                dato_tra = rf['dato_tra']
                total_cobrado = total_transferencia
                total_tarjeta = 0
                total_efectivo = 0
            else:
                total_cobrado = total_efectivo
                total_tarjeta = 0
                total_transferencia = 0
            
            #Comprueba si el numero de documento ya existe
            cursor = pool_db.getCursorSgp()
            cursor.execute('SELECT ci_ruc FROM clientes WHERE ci_ruc = %s', (ci_ruc,))
            cliente = cursor.fetchone()
            cursor.close()

            cursor = pool_db.getCursorSgp()
            cursor.execute('SELECT monto_total FROM factura WHERE nro_factura = %s', (factura,))
            total_factura = cursor.fetchone()[0]
            cursor.close()
            # Si el nombre de usuario ya existe, muestra un mensaje
            if not cliente:
                flash('No existe el cliente ingresado!')
            else:
                if int(total_factura) == int(total_cobrado):
                    cursor = pool_db.getCursorSgp()
                    cursor.execute("INSERT INTO cobros (nro_recibo, ci_ruc, name, tipo_cobro, total_efectivo, total_transferencia, total_tarjeta, total_cobrado, descripcion ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (nro_recibo, ci_ruc, nombre, tipo_cobro, total_efectivo, total_transferencia, total_tarjeta, total_cobrado, descripcion, ))
                    cursor.connection.commit()
                    cursor.close()

                    cursor = pool_db.getCursorSgp()
                    cursor.execute('SELECT max(id) FROM cobros WHERE nro_recibo = %s', (nro_recibo,))
                    det_cobroid = cursor.fetchone()[0]
                    cursor.close()

                    if tipo_cobro == 'Tarjeta':
                        cursor = pool_db.getCursorSgp()
                        cursor.execute("INSERT INTO detalle_cobros (id, nro_factura , total_factura, total_cobrado_fac, pos, nro_cuenta ) VALUES (%s,%s,%s,%s,%s,%s)", (det_cobroid, factura, total_factura, total_tarjeta, dato_tar, '', ))
                        cursor.connection.commit()
                        cursor.close()

                        cursor = pool_db.getCursorSgp()
                        cursor.execute("UPDATE factura SET  condicion_pago=%s WHERE nro_factura = %s",('Cobrado', factura,))
                        cursor.connection.commit()
                        cursor.close()

                    elif tipo_cobro == 'Transferencia':
                        cursor = pool_db.getCursorSgp()
                        cursor.execute("INSERT INTO detalle_cobros (id, nro_factura , total_factura, total_cobrado_fac, pos, nro_cuenta ) VALUES (%s,%s,%s,%s,%s,%s)", (det_cobroid, factura, total_factura, total_transferencia, '', dato_tra, ))
                        cursor.connection.commit()
                        cursor.close()

                        cursor = pool_db.getCursorSgp()
                        cursor.execute("UPDATE factura SET  condicion_pago=%s WHERE nro_factura = %s",('Cobrado', factura,))
                        cursor.connection.commit()
                        cursor.close()
                    else:
                        cursor = pool_db.getCursorSgp()
                        cursor.execute("INSERT INTO detalle_cobros (id, nro_factura , total_factura, total_cobrado_fac, pos, nro_cuenta ) VALUES (%s,%s,%s,%s,%s,%s)", (det_cobroid, factura, total_factura, total_efectivo, '', '', ))
                        cursor.connection.commit()
                        cursor.close()
                    
                        cursor = pool_db.getCursorSgp()
                        cursor.execute("UPDATE factura SET  condicion_pago=%s WHERE nro_factura = %s",('Cobrado', factura,))
                        cursor.connection.commit()
                        cursor.close()

                    flash('Registro exitoso!')
                    return redirect(url_for('views.cobros'))
                elif int(total_factura) > int(total_cobrado):
                    total_factura = int(total_factura) - int(total_cobrado)
                    cursor = pool_db.getCursorSgp()
                    cursor.execute("INSERT INTO cobros (nro_recibo, ci_ruc, name, tipo_cobro, total_efectivo, total_transferencia, total_tarjeta, total_cobrado, descripcion ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (nro_recibo, ci_ruc, nombre, tipo_cobro, total_efectivo, total_transferencia, total_tarjeta, total_cobrado, descripcion, ))
                    cursor.connection.commit()
                    cursor.close()

                    cursor = pool_db.getCursorSgp()
                    cursor.execute('SELECT max(id) FROM cobros WHERE nro_recibo = %s', (nro_recibo,))
                    det_cobroid = cursor.fetchone()[0]
                    cursor.close()

                    if tipo_cobro == 'Tarjeta':
                        cursor = pool_db.getCursorSgp()
                        cursor.execute("INSERT INTO detalle_cobros (id, nro_factura , total_factura, total_cobrado_fac, pos, nro_cuenta ) VALUES (%s,%s,%s,%s,%s,%s)", (det_cobroid, factura, total_factura, total_tarjeta, dato_tar, '', ))
                        cursor.connection.commit()
                        cursor.close()

                        cursor = pool_db.getCursorSgp()
                        cursor.execute("UPDATE factura SET  monto_total=%s WHERE nro_factura = %s",(total_factura, factura,))
                        cursor.connection.commit()
                        cursor.close()

                    elif tipo_cobro == 'Transferencia':
                        cursor = pool_db.getCursorSgp()
                        cursor.execute("INSERT INTO detalle_cobros (id, nro_factura , total_factura, total_cobrado_fac, pos, nro_cuenta ) VALUES (%s,%s,%s,%s,%s,%s)", (det_cobroid, factura, total_factura, total_transferencia, '', dato_tra, ))
                        cursor.connection.commit()
                        cursor.close()

                    else:
                        cursor = pool_db.getCursorSgp()
                        cursor.execute("INSERT INTO detalle_cobros (id, nro_factura , total_factura, total_cobrado_fac, pos, nro_cuenta ) VALUES (%s,%s,%s,%s,%s,%s)", (det_cobroid, factura, total_factura, total_efectivo, '', '', ))
                        cursor.connection.commit()
                        cursor.close()

                    flash('Cobro parcial realizado!')
                    return redirect(url_for('views.cobros'))
                else:
                    flash('Monto ingresado no puede ser superior al monto a cobrar')
                
        elif rm == 'POST':
            # Si el formulario esta vacio...
            flash('Por favor, complete el formulario!')
        return redirect(url_for('views.cobros'))

    def eliminar_cobro(id):
        cursor = pool_db.getCursorSgp()
        cursor.execute("SELECT nro_factura FROM detalle_cobros where id = {0}".format(id))
        factura = cursor.fetchone()[0]
        cursor.close()

        cursor = pool_db.getCursorSgp()
        cursor.execute("SELECT total_cobrado_fac FROM detalle_cobros where id = {0}".format(id))
        cobrado = cursor.fetchone()[0]
        cursor.close()

        cursor = pool_db.getCursorSgp()
        cursor.execute("SELECT total_factura FROM detalle_cobros where id = {0}".format(id))
        total_factura = cursor.fetchone()[0]
        cursor.close()

        total_factura = total_factura + cobrado

        cursor = pool_db.getCursorSgp()
        cursor.execute("DELETE FROM detalle_cobros where id = {0}".format(id))
        cursor.connection.commit()
        cursor.close()

        cursor = pool_db.getCursorSgp()
        cursor.execute("DELETE FROM cobros where id = {0}".format(id))
        cursor.connection.commit()
        cursor.close()

        cursor = pool_db.getCursorSgp()
        cursor.execute("UPDATE factura SET condicion_pago=%s WHERE nro_factura = %s",('Credito', factura,))
        cursor.connection.commit()
        cursor.close()
        flash('Cobro Eliminado Correctamente')

class Pagos:
    def agregar_pago(rm,rf):
        if rm == 'POST' and 'ci_ruc' and 'sgtepago' in rf and 'name' in rf and 'saldo_factura' in rf and 'monto_total' in rf and 'descripcion' in rf and 'nro_factura_compra' and 'tipo_pago' in rf and 'monto_pagar' in rf:
            sgtepago = rf['sgtepago']
            ci_ruc = rf['ci_ruc']
            name = rf['name']
            tipo_pago = rf['tipo_pago']
            saldo_factura = rf['saldo_factura']
            monto_pagar = rf['monto_pagar']
            monto_total = rf['monto_total']
            descripcion = rf['descripcion']
            nro_factura_compra = rf['nro_factura_compra']
            
            if int(saldo_factura)>int(monto_pagar):
                saldo=int(int(saldo_factura)-int(monto_pagar))
                #Se inserta el pago
                cursor = pool_db.getCursorSgp()
                cursor.execute("INSERT INTO pagos (nro_pago, ci_ruc, name,tipo_pago,total_factura,saldo_factura, total_pagado, descripcion) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (sgtepago, ci_ruc,name,tipo_pago, monto_total,saldo,monto_pagar, descripcion, ))
                cursor.connection.commit()
                cursor.close()
                #Se actualiza el saldo factura
                cursor = pool_db.getCursorSgp()
                cursor.execute("UPDATE factura_compra SET  saldo_factura=%s WHERE proveedor_id = %s",(saldo,ci_ruc,))
                cursor.connection.commit()
                cursor.close()
                #Se inserta el detalle del pago
                cursor = pool_db.getCursorSgp()
                cursor.execute("INSERT INTO detalle_pagos (nro_factura, total_factura, total_pagado_fac) VALUES (%s,%s,%s)", (nro_factura_compra, monto_total,monto_pagar, ))
                cursor.connection.commit()
                cursor.close()
                flash('Pago Parcial realizado!')
            elif int(saldo_factura)<int(monto_pagar):
                flash('El monto a pagar el mayor al saldo de la factura!')
            else:
                saldo=int(int(saldo_factura)-int(monto_pagar))
                #Se inserta el pago
                cursor = pool_db.getCursorSgp()
                cursor.execute("INSERT INTO pagos (nro_pago, ci_ruc, name,tipo_pago,total_factura,saldo_factura, total_pagado, descripcion) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (sgtepago, ci_ruc,name,tipo_pago, monto_total,saldo,monto_pagar, descripcion, ))
                cursor.connection.commit()
                cursor.close()
                #Se actualiza el saldo factura
                cursor = pool_db.getCursorSgp()
                cursor.execute("UPDATE factura_compra SET  saldo_factura=%s WHERE proveedor_id = %s",(saldo,ci_ruc,))
                cursor.connection.commit()
                cursor.close()
                #Se inserta el detalle del pago
                cursor = pool_db.getCursorSgp()
                cursor.execute("INSERT INTO detalle_pagos (nro_factura, total_factura, total_pagado_fac) VALUES (%s,%s,%s)", (nro_factura_compra, monto_total,monto_pagar, ))
                cursor.connection.commit()
                cursor.close()
                #Cambia estado de la factura de compra a Pagado
                cursor = pool_db.getCursorSgp()
                cursor.execute("UPDATE factura_compra SET  estado=%s WHERE nro_factura_compra = %s",('Pagado',nro_factura_compra,))
                cursor.connection.commit()
                cursor.close()
                flash('Pago exitoso, ya no quedan deudas para esta factura!')
            return redirect(url_for('views.cobros'))
        elif rm == 'POST':
            # Si el formulario esta vacio...
            flash('Por favor, complete los datos')
        return redirect(url_for('views.cobros'))
    
    def eliminar_pago(id):
        cursor = pool_db.getCursorSgp()
        cursor.execute("DELETE FROM detalle_pagos where id = {0}".format(id))
        cursor.connection.commit()
        cursor.close()
        cursor = pool_db.getCursorSgp()
        cursor.execute("DELETE FROM pagos where id = {0}".format(id))
        cursor.connection.commit()
        cursor.close()
        flash('Pago Eliminado Exitosamente')