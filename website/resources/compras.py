from pickle import NONE
from website.database import pool_db
import datetime
from werkzeug.security import generate_password_hash
from flask import render_template, flash, redirect, url_for, request
import re 
from website.models import Users


class OrdenesCompras():
    def agregar_orden_compra(rm,rf):
        ci_ruc = rf['ci-ruc']
        descripcion = rf['descripcion']
        fecha = rf['fecha']
        id = rf['id']
        user_id = rf['user-id']
        cursor = pool_db.getCursorSgp()
        cursor.execute("INSERT INTO orden_compra (id, descripcion, estado, fecha_pago,proveedor_id,user_id) VALUES (%s,%s,%s,%s,%s,%s)",(id, descripcion, 'Pendiente',fecha,ci_ruc, user_id,))
        cursor.connection.commit()
        cursor.close()
      
        cantidad = 0
        costo = 0
        producto = 0  
        for input in rf:
            if 'cantidadR' in input:
                cantidad = request.form[input]
            elif 'unidad_medidaR' in input:
                cursor = pool_db.getCursorSgp()
                cursor.execute("SELECT val_unidad FROM unidad_medida where desc_unidad_medida = %s",(request.form[input],))
                cursor.connection.commit()
                unidad_medida = cursor.fetchone()[0]
                cursor.close() 
                cursor = pool_db.getCursorSgp()
                cursor.execute("SELECT desc_unidad_medida FROM unidad_medida where desc_unidad_medida = %s",(request.form[input],))
                cursor.connection.commit()
                unidad_medida_tipo = cursor.fetchone()[0]
                cursor.close()
            elif 'productoR' in input:
                cursor = pool_db.getCursorSgp()
                cursor.execute("SELECT id FROM productos where descripcion = %s",(request.form[input],))
                cursor.connection.commit()
                producto = cursor.fetchone()[0]
                cursor.close() 
            elif 'costoR' in input:
                costo = request.form[input]

            if cantidad != 0 and producto != 0 and costo != 0 and unidad_medida !=0:
            
                cursor = pool_db.getCursorSgp()
                cursor.execute("INSERT INTO detalle_orden_compra (id_compra_det, id_producto, cantidad,unidad_medida, precio) VALUES (%s,%s,%s,%s,%s)",(id, producto, cantidad,unidad_medida_tipo, costo,))
                cursor.connection.commit()
                cursor.close()
                cantidad = 0
                costo = 0
                producto = 0 
                unidad_medida = 0
                
               
        flash(' Orden de Compra agregada correctamente')

    def eliminar_orden_compra(id):
        cursor = pool_db.getCursorSgp()
        cursor.execute("DELETE FROM detalle_orden_compra where id_compra_det = {0}".format(id))
        cursor.connection.commit()
        cursor.close()
        cursor = pool_db.getCursorSgp()
        cursor.execute("DELETE FROM orden_compra where id = {0}".format(id))
        cursor.connection.commit()
        cursor.close()
        flash('Orden de Compra eliminado Correctamente')

    def modificar_orden_compra(rm,rf):
        if rm == 'POST' and 'ci-ruc' in rf and 'descripcion' in rf and 'fecha' in rf and 'id' in rf and 'user-id':
            ci_ruc = rf['ci-ruc']
            descripcion = rf['descripcion']
            fecha = rf['fecha']
            id = rf['id']
            user_id = rf['user-id']
            cursor = pool_db.getCursorSgp()
            cursor.execute("UPDATE orden_compra SET descripcion=%s, estado=%s, fecha_pago=%s, proveedor_id=%s, user_id=%s WHERE id = %s",(descripcion, 'Pendiente', fecha,ci_ruc, user_id,id,))
            cursor.connection.commit()
            cursor.close()
            cursor = pool_db.getCursorSgp()
            cursor.execute("DELETE FROM detalle_orden_compra WHERE id_compra_det = %s",(id,))
            cursor.connection.commit()
            cursor.close()

            cantidad = 0
            costo = 0
            producto = 0  
            for input in rf:
                if 'cantidadR' in input:
                    cantidad = request.form[input]
                elif 'productoR' in input:
                    cursor = pool_db.getCursorSgp()
                    cursor.execute("SELECT descripcion FROM productos where codigo = %s",(request.form[input],))
                    cursor.connection.commit()
                    producto = cursor.fetchone()[0]
                    cursor.close() 
                elif 'costoR' in input:
                    costo = request.form[input]

                if cantidad != 0 and producto != 0 and costo != 0:
                    cursor = pool_db.getCursorSgp()
                    cursor.execute("INSERT INTO detalle_orden_compra (id_compra_det, id_producto, cantidad, precio) VALUES (%s,%s,%s,%s)",(id, producto, cantidad, costo,))
                    cursor.connection.commit()
                    cursor.close()
                    cantidad = 0
                    costo = 0
                    producto = 0  
                
            flash('Modificado Correctamente')
        
        #Facturacion Compra

class FacturarCompra():
    def agregar_factura_compra(rm,rf):
        sgtefactura = rf['sgtefactura']
        nro_factura_compra = rf['nro_factura_compra']
        timbrado = rf['timbrado']
        fecha = rf['fecha']
        condicion_pago = rf['condicion_pago']
        id = rf['id']
        ci_ruc = rf['ci-ruc']
        user_id = rf['user-id']
        monto = rf['monto-total']
        #Agrega en la tabla de factura de compra
        cursor = pool_db.getCursorSgp()
        cursor.execute("INSERT INTO factura_compra (id_compra,nro_factura_compra,timbrado,fecha,condicion_pago,monto_total,saldo_factura,ordencompra,estado,proveedor_id,user_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(sgtefactura, nro_factura_compra, timbrado,fecha,condicion_pago,monto,monto,id,'Facturado',ci_ruc, user_id,))
        cursor.connection.commit()
        cursor.close()
        #Cambia estado de orden de compra a Finalizado
        cursor = pool_db.getCursorSgp()
        cursor.execute("UPDATE orden_compra SET  estado=%s,user_id=%s WHERE id = %s",('Finalizado', user_id,id,))
        cursor.connection.commit()
        cursor.close()
       
        cantidad = 0
        costo = 0
        producto = 0  
        unidad_medida_cant = 0
        cant_agregar = 0
        costo_unit = 0
        for input in rf:
            if 'cantidadR' in input:
                cantidad = request.form[input]
            elif 'unidad_medidaR' in input:
                cursor = pool_db.getCursorSgp()
                cursor.execute("SELECT val_unidad FROM unidad_medida where desc_unidad_medida = %s",(request.form[input],))
                cursor.connection.commit()
                unidad_medida_cant = cursor.fetchone()[0]
                cursor.close()

                cursor = pool_db.getCursorSgp()
                cursor.execute("SELECT desc_unidad_medida FROM unidad_medida where desc_unidad_medida = %s",(request.form[input],))
                cursor.connection.commit()
                unidad_medida_tipo = cursor.fetchone()[0]
                cursor.close()
            
            elif 'productoR' in input:
                cursor = pool_db.getCursorSgp()
                cursor.execute("SELECT id FROM productos where descripcion = %s",(request.form[input],))
                cursor.connection.commit()
                producto = cursor.fetchone()[0]
                cursor.close() 
            elif 'costoR' in input:
                costo = request.form[input]

            if cantidad != 0 and producto != 0 and costo != 0 and unidad_medida_cant !=0:
                
                #inserta la factura del detalle de compra
                cursor = pool_db.getCursorSgp()
                cursor.execute("INSERT INTO detalle_factura_compra (id_factura, id_producto, cantidad,unidad_medida, precio) VALUES (%s,%s,%s,%s,%s)",(sgtefactura, producto, cantidad,unidad_medida_tipo, costo,))
                cursor.connection.commit()
                cursor.close()
                #se realiza la actualizacion de la cantidad del producto comprado
                #calcula la cantidad a agregar al inventario segun el calculo de la unidad de medida cargada
                cant_agregar= int(cantidad)*int(unidad_medida_cant)
                cursor = pool_db.getCursorSgp()
                cursor.execute("CALL aumentar_stock(%s,%s);",(producto, cant_agregar,))
                cursor.connection.commit()
                cursor.close()
                #calcula el costo unitario del producto segun la cantidad agregada
                costo_unit=int(int(costo)*int(cantidad))/int (cant_agregar)
                #se realiza el calculo del costo promedio para el producto
                cursor = pool_db.getCursorSgp()
                cursor.execute("CALL calcular_costo(%s,%s,%s,%s);",(costo_unit, cant_agregar, producto,costo,))
                cursor.connection.commit()
                cursor.close()

                cantidad = 0
                costo = 0
                producto = 0 
                unidad_medida_cant = 0
                cant_agregar = 0
                  
               
        flash('Agregado Correctamente')

    def eliminar_factura_compra(id_compra):
        cursor = pool_db.getCursorSgp()
        cursor.execute("DELETE FROM detalle_factura_compra where id_factura = {0}".format(id_compra))
        cursor.connection.commit()
        cursor.close()
        cursor = pool_db.getCursorSgp()
        cursor.execute("DELETE FROM factura_compra where id_compra = {0}".format(id_compra))
        cursor.connection.commit()
        cursor.close()
        flash('Factura de Compra eliminada Correctamente')