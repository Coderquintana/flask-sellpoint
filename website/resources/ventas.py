from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user

from website.database import pool_db
from website.models import Users


class Caja():
    def apertura_caja(rm,rf):
        monto_inicial = int(rf['monto-inicial'])
        user_id = rf['user-id']
        nro_caja = rf['nro-caja']
        cursor = pool_db.getCursorSgp()
        cursor.execute("INSERT INTO caja (monto_inicial, user_id, nro_caja, monto_actual, monto_cierre) VALUES (%s,%s,%s,%s,%s)",(monto_inicial,user_id,nro_caja,monto_inicial,0,))
        cursor.connection.commit()
        cursor.close()
        flash('Agregado Correctamente')

    def eliminar_caja(id):
        cursor = pool_db.getCursorSgp()
        cursor.execute('DELETE FROM caja WHERE id = {0}'.format(id))
        cursor.connection.commit()
        cursor.close()
        flash('Eliminado Correctamente')
    
    def cierre_caja(rm,rf):
        monto_cierre = int(rf['monto-cierre'])
        nro_caja = rf['nro-caj']
        monto_inicial = int(rf['monto-ini'])
        user_caja = int(rf['user-caja'])
        monto_actual = int(rf['monto-act'])
        fecha_cierre = datetime.now()
        if (monto_inicial > monto_cierre) or (monto_cierre != monto_actual):
            flash('Monto no válido')
        else:
            if user_caja != current_user.id:
                flash('Caja de otro usuario')
            else:
                cursor = pool_db.getCursorSgp()
                cursor.execute('UPDATE caja SET monto_cierre = %s, fecha_cierre = %s WHERE nro_caja = %s',(monto_cierre,fecha_cierre, nro_caja,))
                cursor.connection.commit()
                cursor.close()
                flash('Caja Cerrada')

class Pedido():
    def agregar_pedido(rm,rf):
        ci_ruc = rf['ci-ruc']
        user_id = rf['user-id']
        fecha_entrega = rf['fecha-entrega']
        id = rf['sgte-pedido']
        cursor = pool_db.getCursorSgp()
        cursor.execute("INSERT INTO pedido (id, cliente_id, user_id, fecha_entrega, estado) VALUES (%s, %s,%s,%s,%s)",(id, ci_ruc, user_id, fecha_entrega, 1,))
        cursor.connection.commit()
        cursor.close()
      
        cantidad = 0
        precio = 0
        producto = 0  
        for input in rf:
            if 'cantidadR' in input:
                cantidad = request.form[input]
            elif 'productoR' in input:
                cursor = pool_db.getCursorSgp()
                cursor.execute("SELECT id FROM productos where codigo = %s",(request.form[input],))
                cursor.connection.commit()
                producto = cursor.fetchone()[0]
                cursor.close() 
            elif 'precioR' in input:
                precio = request.form[input]

            if cantidad != 0 and producto != 0 and precio != 0:
                cursor = pool_db.getCursorSgp()
                cursor.execute("INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad, precio) VALUES (%s,%s,%s,%s)",(id, producto, cantidad, precio,))
                cursor.connection.commit()
                cursor.close()
                cantidad = 0
                precio = 0
                producto = 0  
               
        flash('Agregado Correctamente')
        
    def eliminar_pedido(id):
        cursor = pool_db.getCursorSgp()
        cursor.execute("DELETE FROM detalle_pedido where id_pedido = {0}".format(id))
        cursor.connection.commit()
        cursor.close()
        cursor = pool_db.getCursorSgp()
        cursor.execute("DELETE FROM pedido where id = {0}".format(id))
        cursor.connection.commit()
        cursor.close()
        flash('Pedido eliminado Correctamente')

    def modificar_pedido(rm,rf):
        ci_ruc = rf['ci-ruc']
        user_id = rf['user-id']
        fecha_entrega = rf['fecha-entrega']
        id = rf['sgte-pedido']
        cursor = pool_db.getCursorSgp()
        cursor.execute("UPDATE pedido SET cliente_id = %s, user_id=%s, fecha_entrega=%s, estado=%s WHERE id = %s",(ci_ruc, user_id, fecha_entrega, 1, id,))
        cursor.connection.commit()
        cursor.close()

        cursor = pool_db.getCursorSgp()
        cursor.execute("DELETE FROM detalle_pedido WHERE id_pedido = %s",(id,))
        cursor.connection.commit()
        cursor.close()

      
        cantidad = 0
        precio = 0
        producto = 0  
        for input in rf:
            if 'cantidadR' in input:
                cantidad = request.form[input]
            elif 'productoR' in input:
                cursor = pool_db.getCursorSgp()
                cursor.execute("SELECT id FROM productos where codigo = %s",(request.form[input],))
                cursor.connection.commit()
                producto = cursor.fetchone()[0]
                cursor.close() 
            elif 'precioR' in input:
                precio = request.form[input]

            if cantidad != 0 and producto != 0 and precio != 0:
                cursor = pool_db.getCursorSgp()
                cursor.execute("INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad, precio) VALUES (%s,%s,%s,%s)",(id, producto, cantidad, precio,))
                cursor.connection.commit()
                cursor.close()
                cantidad = 0
                precio = 0
                producto = 0  
        flash('Agregado Correctamente')   
        
class Factura():
    def agregar_factura(rm,rf):
        ci_ruc = rf['ci-ruc']
        monto = rf['monto-total']
        condicion_pago = request.form['flexRadioDefault']
        if 'flexRadioDefault2' in rf:
            metodo_pago = request.form['flexRadioDefault2']
        else:
            metodo_pago = ''
        if metodo_pago == 'Tarjeta':
            pos = rf['tarje']
            nro_cuenta = ''
        else:
            pos = ''
            nro_cuenta = rf['nro-cuenta']
        es_p = rf['es-pedido']
        pedido = rf['pedido-id']
        if 'delivery-ci' in rf and 'delivery-phone' in rf:
            delivery_ci = rf['delivery-ci']
            delivery_phone = rf['delivery-phone']
        else:
            delivery_ci = ''
            delivery_phone = ''
        es_pedido = False
        pendiente = 'Cobrado'

        if es_p == '1' :
            es_pedido = True

        if delivery_ci != '':
            pendiente = 'Enviado'
        if condicion_pago == 'Credito':
            forma_pago = ''
            cur = pool_db.getCursorSgp()
            cur.execute('UPDATE clientes SET cred_limite = cred_limite - %s WHERE ci_ruc = %s',(monto, ci_ruc,))
            cur.connection.commit()
            cur.close()
        else:
            forma_pago = request.form['flexRadioDefault2'] 
        nro_factura = rf['sgte']
        cur = pool_db.getCursorSgp()
        cur.execute('SELECT nro_caja FROM caja where monto_cierre = 0 and user_id = %s',(current_user.id,))
        nro_caja = cur.fetchone()[0]
        cur.close() 
        id_factura = rf['sgte-factura']
        cursor = pool_db.getCursorSgp()
        cursor.execute("""INSERT INTO factura (id, nro_factura, tipo_comprobante, condicion_pago, forma_pago, monto_total,
            pedido, pedido_id, delivery_ci, delivery_phone, estado, cliente, nro_caja, user_id, anulado, pos, nro_cuenta) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (id_factura,nro_factura,1,condicion_pago,forma_pago,monto,es_pedido,pedido,delivery_ci,delivery_phone,pendiente,ci_ruc,nro_caja,current_user.id,False,pos,nro_cuenta,))
        cursor.connection.commit()
        cursor.close()
        cursor = pool_db.getCursorSgp()
        cursor.execute("UPDATE empresa SET nro_factura = nro_factura + 1")
        cursor.connection.commit()
        cursor.close()
        if delivery_ci == '' and condicion_pago=='Contado' and forma_pago=='Efectivo':
            cursor = pool_db.getCursorSgp()
            cursor.execute("UPDATE pedido SET estado = 0 where id = %s",pedido)
            cursor.connection.commit()
            cursor.close()
            cursor = pool_db.getCursorSgp()
            cursor.execute("CALL aumentar_monto_actual(%s,%s);",(nro_caja, monto))
            cursor.connection.commit()
            cursor.close()
      
        cantidad = 0
        precio = 0
        producto = 0  
        for input in rf:
            if 'cantidadR' in input:
                cantidad = request.form[input]
            elif 'productoR' in input:
                cursor = pool_db.getCursorSgp()
                cursor.execute("SELECT id FROM productos where codigo = %s",(request.form[input],))
                producto = cursor.fetchone()[0]
                cursor.close() 
            elif 'precioR' in input:
                precio = request.form[input]

            if cantidad != 0 and producto != 0 and precio != 0:
                cursor = pool_db.getCursorSgp()
                cursor.execute("INSERT INTO detalle_factura (id_factura, id_producto, cantidad, precio) VALUES (%s,%s,%s,%s)",(id_factura, producto, cantidad, precio,))
                cursor.connection.commit()
                cursor.close()
                cursor = pool_db.getCursorSgp()
                cursor.execute("CALL descontar_stock(%s,%s);",(producto, cantidad,))
                cursor.connection.commit()
                cursor.close()
                cantidad = 0
                precio = 0 
                producto = 0  
        flash('Imprimiendo Factura')
        
    def anular_factura(rm,rf):
        nro_factura = rf['factura-anular']
        cursor = pool_db.getCursorSgp()
        cursor.execute("SELECT id, monto_total, nro_caja, condicion_pago, forma_pago FROM factura WHERE nro_factura = %s AND anulado = %s",(nro_factura,False,))
        fact = cursor.fetchall()
        cursor.close()
        if fact[0][3] == 'Contado' and fact[0][4] == 'Efectivo':
            cursor = pool_db.getCursorSgp()
            cursor.execute("UPDATE caja SET monto_actual = monto_actual - %s WHERE nro_caja = %s",(fact[0][1],fact[0][2],))
            cursor.connection.commit()
            cursor.close()
        if fact:
            cursor = pool_db.getCursorSgp()
            cursor.execute("CALL anular_factura(%s);",(nro_factura,))
            cursor.connection.commit()
            cursor.close()
            flash("Factura Anulada")
        else:
            flash("Factura inválida")