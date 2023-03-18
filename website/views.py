from os import access

from flask import (Blueprint, flash, json, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required

from website.database import pool_db
from website.models import clientes
from website.resources.compras import FacturarCompra, OrdenesCompras
from website.resources.cuentacorriente import Cliente, Cobros, Pagos, Proveedor
from website.resources.stock import (Entrada, Familia, Inventario, Producto,
                                     Salida, Seccion, UnidadMedida)
from website.resources.ventas import Caja, Factura, Pedido

from . import db

views = Blueprint('views', __name__)

#-------------------------------Inicio Sistema-------------------------------------------------

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
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT nro_caja FROM caja where monto_cierre = 0 and user_id = %s',(current_user.id,))
    nro_caja = cur.fetchone()
    cur.close()
    empresa.append(nro_caja)
    return empresa


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    access = Access()
    empresa = Empresa()
    return render_template("home.html", user=current_user, access=access,empresa=empresa, caja=caja)

#-------------------------------Ventas-------------------------------------------------

@views.route('/registrar_venta', methods=['GET', 'POST'])
def registrarVenta():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM clientes')
    list_cliente = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute("""SELECT * FROM productos prod
                    left join (select pr.codigo as cod, pr.fecha_inicio, pr.fecha_fin from promocion pr) aux
                    on aux.cod = prod.codigo
                    where current_date between aux.fecha_inicio and aux.fecha_fin
                    or prod.descripcion not like '%Combo%'""")
    list_productos = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute("SELECT p.id, p.estado, p.fecha_entrega, p.cliente_id, p.user_id, c.name FROM pedido p join clientes c on c.ci_ruc = p.cliente_id where p.estado = '1' and p.fecha_entrega = current_date")
    list_pedido = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT id FROM caja where monto_cierre = 0 and user_id = %s',(current_user.id,))
    caja = cur.fetchone()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT COALESCE(MAX(id), 0) + 1 as id FROM factura')
    sgte_factura  = cur.fetchone()[0]
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT nro_factura + 1, timbrado sgte FROM empresa')
    datos  = cur.fetchone()
    cur = pool_db.getCursorSgp()
    cur.execute("select codigo from promocion where current_date between fecha_inicio and fecha_fin")
    if cur:
        promo = cur.fetchone()
        cur.close()
    else:
        promo = ''
    if caja:
        return render_template('registrar_venta.html', user=current_user, access=access, empresa=empresa,
        list_cliente=list_cliente, list_productos=list_productos,list_pedido=list_pedido,sgte_factura=sgte_factura,
        datos=datos,promo=promo)
    else:
        flash('Debe abrir una caja')
        return redirect(url_for('views.home'))
    
@views.route('/agregar_factura', methods=['GET', 'POST'])
def agregarFactura():
    for input in request.form:
        if 'cantidadR' in input:
            detalle = request.form[input]
    if detalle:
        Factura.agregar_factura(request.method,request.form)
        return redirect(url_for('views.registrarVenta'))
    else:
        flash("Factura sin detalles")
        return redirect(url_for('views.registrarVenta'))

@views.route('/eliminar_factura/<int:id>', methods=['GET', 'POST'])
def eliminarFactura(id):
    Factura.eliminar_factura(id)
    return redirect(url_for('views.pedidos'))

@views.route('/anular_factura', methods=['GET', 'POST'])
def anularFactura():
    Factura.anular_factura(request.method,request.form)
    return redirect(url_for('views.registrarVenta'))



@views.route('/caja', methods=['GET', 'POST'])
def caja():
    access = Access()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM caja')
    list_caja = cur.fetchall()
    cur.close()
    empresa = Empresa()
    return render_template('caja.html', user=current_user, access=access, list_caja=list_caja, empresa=empresa)

@views.route('/apertura_caja', methods=['POST', 'GET'])
def aperturaCaja():
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT nro_caja FROM caja where monto_cierre = 0 and user_id = %s',(current_user.id,))
    c_caja = cur.fetchall()
    cur.close()
    if c_caja:
        flash("Usuario ya cuenta con una caja activa")
        return redirect(url_for('views.caja'))
    else:
        Caja.apertura_caja(request.method,request.form)
        return redirect(url_for('views.caja'))

@views.route('/eliminar_caja/<int:id>', methods=['POST', 'GET'])
def eliminarCaja(id):
    Caja.eliminar_caja(id)
    return redirect(url_for('views.caja'))

@views.route('/cierre_caja', methods=['POST', 'GET'])
def cierreCaja():
    Caja.cierre_caja(request.method,request.form)
    return redirect(url_for('views.caja'))

@views.route('/registrar_cobro', methods=['POST', 'GET'])
def registrarCobro():
    empresa = Empresa()
    factura = request.form['factura-enviada']
    cur = pool_db.getCursorSgp()
    cur.execute("SELECT id, monto_total FROM factura where nro_factura = %s and estado = 'Enviado'",(factura,))
    fact = cur.fetchone()
    cur.close()
    if fact:
        cur = pool_db.getCursorSgp()
        cur.execute("CALL aumentar_monto_actual(%s,%s);",(empresa[11][0], fact[1],))
        cur.connection.commit()
        cur.close()
        cur = pool_db.getCursorSgp()
        cur.execute("UPDATE factura SET estado = 'Cobrado' WHERE nro_factura = %s",(factura,))
        cur.connection.commit()
        cur.close()
        flash("Factura cobrada")
    else:
        flash("Factura Inválida")
    return redirect(url_for('views.caja'))

@views.route('/selectcaja', methods=['GET', 'POST'])
def selectcaja():   
    if request.method == 'POST': 
        nro_caja = request.form['nro_caja']
        cur = pool_db.getCursorSgp()
        result = cur.execute("SELECT * FROM caja c join users u on c.user_id=u.id WHERE nro_caja = %s", [nro_caja])
        rscaja = cur.fetchall()
        cur.close()
        cajaarray = []
        for rs in rscaja:
            caja_dict = {
                'id': rs['id'],
                'user_id':rs['user_id'],
                'user_name':rs['name'],
                'nro_caja': rs['nro_caja'],
                'fecha': rs['fecha'],
                'fecha_cierre':rs['fecha_cierre'],
                'monto_inicial': rs['monto_inicial'],
                'monto_actual': rs['monto_actual'],
                'monto_cierre': rs['monto_cierre']}
            cajaarray.append(caja_dict)
        return json.dumps(cajaarray)

    
@views.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM clientes')
    list_cliente = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM productos')
    list_productos = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM pedido')
    list_pedido = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT COALESCE(MAX(id), 0) + 1 as id FROM pedido')
    sgte_pedido  = cur.fetchone()
    data = sgte_pedido[0]
    data2 = int(data)
    cur.close()
    return render_template('pedidos.html', user=current_user, access=access, list_cliente=list_cliente,
                list_productos=list_productos, list_pedido=list_pedido, data2=data2, empresa=empresa)

@views.route('/selectfactura', methods=['GET', 'POST'])
def selectfacturas():   
    if request.method == 'POST': 
        factura = request.form['id']
        cur = pool_db.getCursorSgp()
        result = cur.execute("SELECT *, f.id as fid, f.estado as festado FROM factura f join clientes c on c.ci_ruc = f.cliente WHERE nro_factura = %s", [factura,])
        rsfactura = cur.fetchall()
        cur.close()
        facturaarray = []
        for rs in rsfactura:
            pedido_dict = { 
                'id': rs['fid'],
                'nro_factura': rs['nro_factura'],
                'estado': rs['festado'],
                'cliente': rs['name'],
                'pedido_id': rs['pedido_id'],
                'pos':rs['pos'],
                'nro_cuenta':rs['nro_cuenta'],
                'delivery_ci':rs['delivery_ci'],
                'delivery_phone':rs['delivery_phone'],
                'monto_total': rs['monto_total'],
                'user_id': rs['user_id']}
            facturaarray.append(pedido_dict)
        return json.dumps(facturaarray)

    
@views.route('/selectcajafactura', methods=['GET', 'POST'])
def selectcajafactura():   
    if request.method == 'POST': 
        nro_caja = request.form['nro_caja']
        cur = pool_db.getCursorSgp()
        result = cur.execute("SELECT * from factura f join clientes c on c.ci_ruc = f.cliente where f.nro_caja = %s and condicion_pago = 'Contado' and f.estado = 'Cobrado' and anulado = False", (nro_caja,))
        rscajafactura = cur.fetchall()
        cur.close()
        cajafacturaarray = []
        for rs in rscajafactura:
            cajafactura_dict = { 
                'nro_factura': rs['nro_factura'],
                'cliente': rs['name'],
                'monto_total': rs['monto_total'],
                'nro_caja': rs['nro_caja'],
                'forma_pago': rs['forma_pago']}
            cajafacturaarray.append(cajafactura_dict)
        return json.dumps(cajafacturaarray)

@views.route('/selectdetallefactura', methods=['GET', 'POST'])
def selectdetallefactura():   
    if request.method == 'POST': 
        factura = request.form['facturaid']
        cur = pool_db.getCursorSgp()
        result = cur.execute("SELECT * , df.cantidad as cant FROM detalle_factura df join productos p on p.id = df.id_producto WHERE id_factura = %s", [factura,])
        rsfactura = cur.fetchall()
        cur.close()
        facturaarray = []
        for rs in rsfactura:
            pedido_dict = {
                'id_producto': rs['descripcion'],
                'cantidad': rs['cant'],
                'precio': rs['precio']}
            facturaarray.append(pedido_dict)
        return json.dumps(facturaarray)

@views.route('/selectcliente', methods=['GET', 'POST'])
def selectcliente():   
    if request.method == 'POST': 
        ci_ruc = request.form['ci_ruc']
        cur = pool_db.getCursorSgp()
        result = cur.execute("SELECT * FROM clientes WHERE ci_ruc = %s", [ci_ruc])
        rscliente = cur.fetchall()
        cur.close()
        clientearray = []
        for rs in rscliente:
            cliente_dict = {
                'id': rs['id'],
                'city': rs['city'],
                'phone': rs['phone'],
                'email': rs['email'],
                'address': rs['address'],
                'name': rs['name'],
                'limite': rs['cred_limite'],
                'ci_ruc': rs['ci_ruc']}
            clientearray.append(cliente_dict)
        return json.dumps(clientearray)

@views.route('/selectproducto', methods=['GET', 'POST'])
def selectproducto():   
    if request.method == 'POST': 
        prod = request.form['prod']
        cur = pool_db.getCursorSgp()
        result = cur.execute("""select p.id, p.precio1, p.precio_promo, p.precio_mayor, p.tipo_impuesto, 
                    p.unidad_medida_venta, p.descripcion, p.familia, tp.desc_tipo_impuesto from productos p
                    join tipo_impuesto tp
                    on tp.id = p.tipo_impuesto
                    where p.codigo = %s""", [prod])
        rsproducto = cur.fetchall()
        cur.close()
        productoarray = []
        for rs in rsproducto:
            producto_dict = {
                'id': rs['id'],
                'precio1': rs['precio1'],
                'precio_promo': rs['precio_promo'],
                'precio_mayor': rs['precio_mayor'],
                'tipo_impuesto': rs['desc_tipo_impuesto'],
                'unidad_medida': rs['unidad_medida_venta'],
                'descripcion': rs['descripcion'],
                'familia': rs['familia']}
            productoarray.append(producto_dict)
        return json.dumps(productoarray)

@views.route('/selectpedido', methods=['GET', 'POST'])
def selectpedido():   
    if request.method == 'POST': 
        pedido = request.form['pedido']
        cur = pool_db.getCursorSgp()
        result = cur.execute("SELECT * FROM pedido WHERE id = %s", [pedido])
        rspedido = cur.fetchall()
        cur.close()
        pedidoarray = []
        for rs in rspedido:
            pedido_dict = {
                'id': rs['id'],
                'ci_ruc': rs['cliente_id'],
                'estado': rs['estado'],
                'fecha_registro': rs['fecha_registro'],
                'fecha_entrega': rs['fecha_entrega'],
                'user_id': rs['user_id']}
            pedidoarray.append(pedido_dict)
        return json.dumps(pedidoarray)
    
@views.route('/selectdetalle', methods=['GET', 'POST'])
def selectdetalle():   
    if request.method == 'POST': 
        pedido = request.form['pedido']
        cur = pool_db.getCursorSgp()
        result = cur.execute("""SELECT p.codigo, p.descripcion, tp.desc_tipo_impuesto, dp.cantidad, dp.precio FROM detalle_pedido dp
                                JOIN productos p
                                ON p.id = dp.id_producto 
                                join tipo_impuesto tp
                                on tp.id = p.tipo_impuesto
                                WHERE id_pedido = %s""", [pedido])
        rsdetalle = cur.fetchall()
        cur.close()
        detallearray = []
        for rs in rsdetalle:
            detalle_dict = {
                'codigo': rs['codigo'],
                'descripcion': rs['descripcion'],
                'cantidad': rs['cantidad'],
                'tipo_impuesto': rs['desc_tipo_impuesto'],
                'precio': rs['precio']}
            detallearray.append(detalle_dict)
        return json.dumps(detallearray)
    
@views.route('/selectpromocion', methods=['GET', 'POST'])
def selectpromocion():   
    if request.method == 'POST': 
        prom = request.form['prom']
        cur = pool_db.getCursorSgp()
        cur.execute("""select pr.codigo, prod.codigo as prods, pr.cantidad1 from productos prod
                        join promocion pr
                        on prod.codigo = pr.producto1
                        or prod.codigo = pr.producto2
                        where pr.codigo = %s""",(prom,))
        rsprom = cur.fetchall()
        cur.close()
        promarray = []          
        for rs in rsprom:
            prom_dict = {
                'codigo': rs['codigo'],
                'cantidad1': rs['cantidad1'],
                'prods': rs['prods']}
            promarray.append(prom_dict)
        return json.dumps(promarray)

@views.route('/agregar_pedido', methods=['GET', 'POST'])
def agregarPedido():
    Pedido.agregar_pedido(request.method,request.form)
    return redirect(url_for('views.pedidos'))

@views.route('/eliminar_pedido/<int:id>', methods=['GET', 'POST'])
def eliminarPedido(id):
    Pedido.eliminar_pedido(id)
    return redirect(url_for('views.pedidos'))

@views.route('/modificar_pedido', methods=['GET', 'POST'])
def modificarPedido():
    Pedido.modificar_pedido(request.method,request.form)
    return redirect(url_for('views.pedidos'))


@views.route('/reporte_ventas', methods=['GET', 'POST'])
def reporteVentas():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT *,f.id as fid FROM factura f join clientes c on c.ci_ruc = f.cliente')
    list_facturas = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute("SELECT * , df.cantidad as cant FROM detalle_factura df join productos p on p.id = df.id_producto")
    list_det_fact = cur.fetchall()
    cur.close()
    return render_template('reporte_ventas.html', user=current_user, access=access, empresa=empresa, 
        list_facturas=list_facturas,list_det_fact=list_det_fact)

@views.route('/reporte_caja', methods=['GET', 'POST'])
def reporteCaja():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM caja')
    list_caja = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM factura')
    list_facturas = cur.fetchall()
    cur.close()
    return render_template('reporte_caja.html', user=current_user, access=access, empresa=empresa, 
        list_caja=list_caja, list_facturas=list_facturas)

@views.route('/reporte_pedido', methods=['GET', 'POST'])
def reportePedido():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM pedido')
    list_pedido = cur.fetchall()
    cur.close()
    return render_template('reporte_pedido.html', user=current_user, access=access, empresa=empresa, list_pedido=list_pedido)
#-------------------------------Compras-------------------------------------------------

@views.route('/compras', methods=['GET', 'POST'])
def FacturacionCompra():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM proveedores')
    list_proveedores = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM productos')
    list_productos = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute("SELECT * FROM orden_compra where estado='Pendiente'")
    list_oc_edit = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT MAX(id) + 1 as id FROM orden_compra')
    list_orden_compras = cur.fetchone()[0]
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT COALESCE(MAX(id_compra), 0) + 1 as id FROM factura_compra')
    sgtefactura  = cur.fetchone()
    data = sgtefactura[0]
    data2 = int(data)
    cur.close()
    return render_template('compras.html', user=current_user, empresa=empresa, access=access, list_proveedores=list_proveedores,
                list_productos=list_productos,list_orden_compras=list_orden_compras,list_oc_edit=list_oc_edit,data2=data2)

@views.route('/selectproductocompra', methods=['GET', 'POST'])
def selectproductocompra():   
    if request.method == 'POST': 
        prod = request.form['prod']
        cur = pool_db.getCursorSgp()
        result = cur.execute("""select p.id,p.costo, p.precio1, p.tipo_impuesto, p.unidad_medida_venta, p.descripcion, 
                    p.familia, tp.desc_tipo_impuesto from productos p
                    join tipo_impuesto tp
                    on tp.id = p.tipo_impuesto
                    where p.codigo = %s""", [prod])
        rsproducto = cur.fetchall()
        cur.close()
        productoarray = []
        for rs in rsproducto:
            producto_dict = {
                'id': rs['id'],
                'costo': rs['costo'],
                'precio1': rs['precio1'],
                'tipo_impuesto': rs['desc_tipo_impuesto'],
                'unidad_medida': rs['unidad_medida_venta'],
                'descripcion': rs['descripcion'],
                'familia': rs['familia']}
            productoarray.append(producto_dict)
        return json.dumps(productoarray)    
   
@views.route('/ordencompra', methods=['GET', 'POST'])
def VerOrdenCompras():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute("SELECT oc.id,p.name,oc.descripcion,to_char(oc.fecha_registro,'DD/MM/YYYY') AS fecha_registro,oc.estado FROM orden_compra oc, proveedores p where oc.proveedor_id=p.ci_ruc order by id desc")
    list_orden_compras = cur.fetchall()
    cur.close()
    return render_template('ordencompra.html', user=current_user, list_orden_compras = list_orden_compras,access=access, empresa=empresa)

@views.route('/generarordencompra', methods=['GET', 'POST'])
def OrdenCompra():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM proveedores')
    list_proveedores = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM productos')
    list_productos = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM unidad_medida')
    list_unidad_medida = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute("SELECT * FROM orden_compra where estado='Pendiente'")
    list_oc_edit = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT MAX(id) + 1 as id FROM orden_compra')
    list_orden_compras = cur.fetchone()[0]
    cur.close()
    return render_template('generarordencompra.html', user=current_user, access=access, empresa=empresa, list_proveedores=list_proveedores,
                list_productos=list_productos,list_orden_compras=list_orden_compras,list_unidad_medida=list_unidad_medida,list_oc_edit=list_oc_edit)

@views.route('/agregar_orden_compra', methods=['GET', 'POST'])
def agregarOrdenCompra():
    OrdenesCompras.agregar_orden_compra(request.method,request.form)
    return redirect(url_for('views.VerOrdenCompras'))

@views.route('/eliminar_orden_compra/<int:id>', methods=['GET', 'POST'])
def eliminarOrdenCompra(id):
    OrdenesCompras.eliminar_orden_compra(id)
    return redirect(url_for('views.VerOrdenCompras'))

@views.route('/modificar_orden_compra', methods=['GET', 'POST'])
def modificarOrdenCompra():
    OrdenesCompras.modificar_orden_compra(request.method,request.form)
    return redirect(url_for('views.VerOrdenCompras'))

@views.route('/facturar_compra', methods=['GET', 'POST'])
def FacturarOrdenCompra():
    for input in request.form:
        if 'cantidadR' in input:
            detalle = request.form[input]
    if detalle:
        FacturarCompra.agregar_factura_compra(request.method,request.form)
        return redirect(url_for('views.reporteCompras'))
    else:
        flash("Factura sin detalles")
        return redirect(url_for('views.FacturacionCompra'))

@views.route('/eliminar_factura_compra/<int:id_compra>', methods=['GET', 'POST'])
def EliminarFacturaCompra(id_compra):
    FacturarCompra.eliminar_factura_compra(id_compra)
    return redirect(url_for('views.reporteCompras'))

@views.route('/reporteprodcompras', methods=['GET', 'POST'])
def reporteProdCompras():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute("select sum((df.cantidad*u.val_unidad)) AS Cantidad,p.descripcion from detalle_factura_compra df,productos p, unidad_medida u where df.id_producto=p.id and df.unidad_medida=u.desc_unidad_medida group by descripcion order by 1 desc")
    list_reporte_compra = cur.fetchall()
    cur.close()
    return render_template('reporteprodcompras.html', user=current_user, list_reporte_compra=list_reporte_compra, access=access, empresa=empresa)


@views.route('/selectordencompra', methods=['GET', 'POST'])
def selectordencompra():   
    if request.method == 'POST': 
        orden_compra = request.form['orden_compra']
        cur = pool_db.getCursorSgp()
        result = cur.execute("SELECT * FROM orden_compra WHERE id = %s", [orden_compra])
        rsordencompra = cur.fetchall()
        cur.close()
        ordencompraarray = []
        for rs in rsordencompra:
            ordencompra_dict = {
                'id': rs['id'],
                'descripcion': rs['descripcion'],
                'ci_ruc': rs['proveedor_id'],
                'estado': rs['estado'],
                'fecha_registro': rs['fecha_registro'],
                'fecha_pago': rs['fecha_pago'],
                'user_id': rs['user_id']}
            ordencompraarray.append(ordencompra_dict)
        return json.dumps(ordencompraarray)

@views.route('/selectdetalleordencompra', methods=['GET', 'POST'])
def selectdetalleordencompra():   
    if request.method == 'POST': 
        orden_compra = request.form['orden_compra']
        cur = pool_db.getCursorSgp()
        result = cur.execute("""SELECT p.descripcion, doc.cantidad, doc.precio, doc.unidad_medida FROM detalle_orden_compra doc
                                JOIN productos p
                                ON p.id = doc.id_producto WHERE id_compra_det = %s""", [orden_compra])
        rsdetalle = cur.fetchall()
        cur.close()
        detallearray = []
        for rs in rsdetalle:
            detalle_dict = {
                'descripcion': rs['descripcion'],
                'cantidad': rs['cantidad'],
                'unidad_medida': rs['unidad_medida'],
                'precio': rs['precio']}
            detallearray.append(detalle_dict)
        return json.dumps(detallearray)

@views.route('/selectdetallefacturacompra', methods=['GET', 'POST'])
def selectdetallefacturacompra():   
    if request.method == 'POST': 
        id_compra = id_compra.form['factura_compra']
        cur = pool_db.getCursorSgp()
        result = cur.execute("""SELECT p.descripcion, dfc.cantidad, dfc.precio,dfc.unidad_medida FROM detalle_factura_compra dfc
                                JOIN productos p
                                ON p.id = dfc.id_producto WHERE id_factura = %s""", [id_compra])
        rsdetalle = cur.fetchall()
        cur.close()
        detallearray = []
        for rs in rsdetalle:
            detalle_dict = {
                'descripcion': rs['descripcion'],
                'cantidad': rs['cantidad'],
                'unidad_medida': rs['unidad_medida'],
                'precio': rs['precio']}
            detallearray.append(detalle_dict)
        return json.dumps(detallearray)



@views.route('/reporte_compras', methods=['GET', 'POST'])
def reporteCompras():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM proveedores')
    list_proveedores = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM productos')
    list_productos = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM orden_compra')
    list_oc_edit = cur.fetchall()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute("SELECT fc.id_compra,fc.nro_factura_compra,p.ci_ruc,p.name,to_char(fc.fecha,'DD/MM/YYYY') AS fecha,fc.monto_total,fc.condicion_pago, fc.estado FROM FACTURA_COMPRA fc, proveedores p where fc.proveedor_id=p.ci_ruc order by fc.id_compra desc")
    list_factura_compra = cur.fetchall()
    cur.close()
    return render_template('reporte_compras.html', user=current_user, access=access, empresa=empresa, list_proveedores=list_proveedores,
                list_productos=list_productos,list_factura_compra=list_factura_compra,list_oc_edit=list_oc_edit)

@views.route('/selectdetallefacturacomprareporte', methods=['GET', 'POST'])
def selectdetallefacturacomprareporte():   
    if request.method == 'POST': 
        factura = request.form['facturaid']
        cur = pool_db.getCursorSgp()
        result = cur.execute("""SELECT p.descripcion, dfc.cantidad, dfc.precio,dfc.unidad_medida FROM detalle_factura_compra dfc
                                JOIN productos p
                                ON p.id = dfc.id_producto WHERE id_factura = %s""", [factura])
        rsdetalle = cur.fetchall()
        cur.close()
        detallearray = []
        for rs in rsdetalle:
            detalle_dict = {
                'descripcion': rs['descripcion'],
                'cantidad': rs['cantidad'],
                'unidad_medida': rs['unidad_medida'],
                'precio': rs['precio']}
            detallearray.append(detalle_dict)
        return json.dumps(detallearray)

#-------------------------------Clientes-------------------------------------------------

@views.route('/clientes', methods=['GET', 'POST'])
def clientes():
    access = Access()
    empresa = Empresa()
    ##Se obtiene los datos de la tabla para ver los tipo de documentos cargados
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM tipo_documento')
    list_tipo_documento = cur.fetchall()
    cur.close()
    ##Se obtiene los datos de la tabla para ver los estados posibles
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM estado_cliente')
    list_estado_cliente = cur.fetchall()
    cur.close()

    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from clientes')
    list_clientes = cur.fetchall()
    cur.close()
    return render_template('clientes.html', user=current_user, list_clientes = list_clientes, access=access,
    list_tipo_documento = list_tipo_documento, list_estado_cliente = list_estado_cliente, empresa=empresa )

@views.route('/agregar_cliente', methods=['POST', 'GET'])
def agregarCliente():
    Cliente.agregar_cliente(request.method,request.form)
    return redirect(url_for('views.clientes'))

@views.route('/editar_cliente', methods=['POST', 'GET'])
def editarCliente():
    Cliente.editar_cliente(request.method,request.form)
    return redirect(url_for('views.clientes'))

@views.route('/tipo_documento', methods=['GET', 'POST'])
def tipo_documento():
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from tipo_documento')
    list_tipo_documento = cur.fetchall()
    cur.close()
    return render_template('clientes.html', 'proveedores.html', list_tipo_documento = list_tipo_documento)

@views.route('/estado_cliente', methods=['GET', 'POST'])
def estado_cliente():
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from estado_cliente')
    list_estado_cliente = cur.fetchall()
    cur.close()
    return render_template('clientes.html', list_estado_cliente = list_estado_cliente)

@views.route('/cobros', methods=['GET', 'POST'])
def cobros():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from cobros')
    list_cobros = cur.fetchall()
    cur.close()

    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from clientes')
    list_clientes = cur.fetchall()
    cur.close()

    return render_template('cobros.html', user=current_user, list_cobros = list_cobros, list_clientes = list_clientes, access = access, empresa = empresa)

@views.route('/agregar_cobro', methods=['POST', 'GET'])
def agregarCobro():
    Cobros.agregar_cobro(request.method,request.form)
    return redirect(url_for('views.cobros'))

@views.route('/eliminar_cobro/<int:id>', methods=['POST', 'GET'])
def eliminarCobros(id):
    Cobros.eliminar_cobro(id)
    return redirect(url_for('views.cobros'))

@views.route('/selectcliente2', methods=['GET', 'POST'])
def selectcliente2():   
    if request.method == 'POST': 
        ci_ruc = request.form['ci_ruc']
        cur = pool_db.getCursorSgp()
        result = cur.execute("SELECT * FROM clientes WHERE ci_ruc = %s", [ci_ruc])
        rscliente = cur.fetchall()
        cur.close()
        clientearray = []
        for rs in rscliente:
            cliente_dict = {
                'id': rs['id'],
                'name': rs['name'],
                'ci_ruc': rs['ci_ruc']}
            clientearray.append(cliente_dict)
        return json.dumps(clientearray)

@views.route('/selectfactura2', methods=['GET', 'POST'])
def selectfactura2():   
    if request.method == 'POST': 
        ci_ruc = request.form['ci_ruc']
        print(ci_ruc)
        cur = pool_db.getCursorSgp()
        result = cur.execute("""select case when d.total_factura is null then f.monto_total else d.total_factura end monto_total, f.id, f.nro_factura
                              from factura f left join detalle_cobros d
                              on f.nro_Factura = d.nro_Factura
                              where f.condicion_pago = 'Credito' and f.cliente = %s""", [ci_ruc])
        rsfactura = cur.fetchall()
        cur.close()
        facturaarray = []
        for rs in rsfactura:
            factura_dict = {
                'id': rs['id'],
                'nro_factura': rs['nro_factura'],
                'monto': rs['monto_total']}
            facturaarray.append(factura_dict)
        return json.dumps(facturaarray)

@views.route('/reporte_cobro', methods=['GET', 'POST'])
def reporteCobro():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute("""SELECT c.name, f.nro_factura, f.condicion_pago, case when d.total_factura is null then f.monto_total else f.monto_total - d.total_cobrado_fac end monto_total, 
                  f.fecha FROM factura f join clientes c 
                  on c.ci_ruc = f.cliente
                  left join detalle_cobros d
                  on  f.nro_factura = d.nro_factura
                  where f.condicion_pago in ('Credito', 'Cobrado')""")
    list_facturas = cur.fetchall()
    cur.close()
    return render_template('reporte_cobro.html', user=current_user, access=access, empresa=empresa, list_facturas=list_facturas)

#-------------------------------Proveedores-------------------------------------------------

@views.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    access = Access()
    empresa = Empresa()
    
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM tipo_documento')
    list_tipo_documento = cur.fetchall()
    cur.close()

    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from proveedores')
    list_proveedores = cur.fetchall()
    cur.close()
    return render_template('proveedores.html', user=current_user, list_proveedores = list_proveedores, 
        list_tipo_documento = list_tipo_documento, access = access, empresa=empresa )

@views.route('/agregar_proveedor', methods=['POST', 'GET'])
def agregarProveedor():
    Proveedor.agregar_proveedor(request.method,request.form)
    return redirect(url_for('views.proveedores'))

@views.route('/editar_proveedor', methods=['POST', 'GET'])
def editarProveedor():
    Proveedor.editar_proveedor(request.method,request.form)
    return redirect(url_for('views.proveedores'))

@views.route('/pagos', methods=['GET', 'POST'])
def pagos():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute("select id,ci_ruc,name,descripcion,total_pagado,to_char(CREATION_DATE,'DD/MM/YYYY') AS CREATION_DATE from pagos ORDER BY CREATION_DATE DESC")
    list_pagos = cur.fetchall()
    cur.close()

    cur = pool_db.getCursorSgp()
    cur.execute("SELECT p.ci_ruc,p.name,fc.nro_factura_compra,fc.fecha,fc.monto_total,fc.condicion_pago from proveedores p join factura_compra fc on p.ci_ruc=fc.proveedor_id and fc.condicion_pago='Credito' and fc.estado='Facturado'")
    list_proveedor = cur.fetchall()
    cur.close()

    cur = pool_db.getCursorSgp()
    cur.execute("SELECT count(*) FROM factura_compra WHERE  condicion_pago = 'Credito' and estado='Facturado'")
    fact_pend  = cur.fetchone()[0]
    cur.close()

    cur = pool_db.getCursorSgp()
    cur.execute("SELECT to_char(fc.fecha,'DD/MM/YYYY') as fecha,p.name,fc.nro_factura_compra, fc.monto_total,fc.saldo_factura FROM factura_compra fc, proveedores p WHERE  fc.condicion_pago = 'Credito' and fc.estado='Facturado'and fc.proveedor_id=p.ci_ruc order by fecha asc")
    pagos_pendientes  = cur.fetchall()
    cur.close()

    cur = pool_db.getCursorSgp()
    cur.execute('SELECT COALESCE(MAX(id), 0) + 1 as id FROM pagos')
    sgtepago  = cur.fetchone()
    data = sgtepago[0]
    data2 = int(data)
    cur.close()
    return render_template('pagos.html', user=current_user, list_pagos = list_pagos,fact_pend=fact_pend, list_proveedor = list_proveedor,pagos_pendientes=pagos_pendientes, data2=data2, access = access, empresa = empresa)
    
@views.route('/selectproveedor', methods=['GET', 'POST'])
def selectproveedor():   
    if request.method == 'POST': 
        ci_ruc = request.form['ci_ruc']
        cur = pool_db.getCursorSgp()
        result = cur.execute("SELECT * FROM proveedores WHERE ci_ruc = %s", [ci_ruc])
        rsproveedor = cur.fetchall()
        cur.close()
        proveedorarray = []
        for rs in rsproveedor:
            proveedor_dict = {
                'id': rs['id'],
                'name': rs['name'],
                'phone': rs['phone'],
                'address': rs['address'],
                'email': rs['email'],
                'city': rs['city'],
                'ci_ruc': rs['ci_ruc']}
            proveedorarray.append(proveedor_dict)
        return json.dumps(proveedorarray)

@views.route('/agregar_pago', methods=['POST', 'GET'])
def agregarPago():
    Pagos.agregar_pago(request.method,request.form)
    return redirect(url_for('views.pagos'))

@views.route('/editar_pagos', methods=['POST', 'GET'])
def editarPago():
    Pagos.editar_pagos(request.method,request.form)
    return redirect(url_for('views.pagos'))
    
@views.route('/eliminar_pago/<int:id>', methods=['GET', 'POST'])
def eliminarPago(id):
    Pagos.eliminar_pago(id)
    return redirect(url_for('views.pagos'))

@views.route('/selectfactura_com', methods=['GET', 'POST'])
def selectfactura_com():   
    if request.method == 'POST': 
        ci_ruc = request.form['ci_ruc']
        cur = pool_db.getCursorSgp()
        result = cur.execute("SELECT * FROM factura_compra WHERE proveedor_id = %s and condicion_pago = 'Credito' and estado='Facturado'", [ci_ruc])
        rsfactura = cur.fetchall()
        cur.close()
        facturaarray = []
        for rs in rsfactura:
            factura_dict = {
                'nro_factura_compra': rs['nro_factura_compra'],
                'fecha': rs['fecha'],
                'monto_total': rs['monto_total'],
                'saldo_factura': rs['saldo_factura']}
            facturaarray.append(factura_dict)
        return json.dumps(facturaarray)

@views.route('/selectfactura_compra', methods=['GET', 'POST'])
def selectfacturacompra():   
    if request.method == 'POST': 
        factura = request.form['id']
        cur = pool_db.getCursorSgp()
        result = cur.execute("SELECT *, f.id_compra as fid, f.estado as festado FROM factura_compra f join proveedores p on p.ci_ruc = f.proveedor_id WHERE f.nro_factura_compra = %s", [factura,])
        rsfactura = cur.fetchall()
        cur.close()
        facturaarray = []
        for rs in rsfactura:
            pedido_dict = { 
                'id_compra': rs['fid'],
                'nro_factura_compra': rs['nro_factura_compra'],
                'name': rs['name'],
                'monto_total': rs['monto_total']}
            facturaarray.append(pedido_dict)
        return json.dumps(facturaarray)

#-------------------------------Productos-------------------------------------------------

@views.route('/productos', methods=['GET', 'POST'])
def productos():
    access = Access()
    empresa = Empresa()

    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM productos')
    list_productos = cur.fetchall()
    cur.close()

    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from unidad_medida')
    list_unidad_medida = cur.fetchall()
    cur.close()

    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from tipo_impuesto')
    list_tipo_impuesto = cur.fetchall()
    cur.close()

    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from familia')
    list_familia = cur.fetchall()
    cur.close()

    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from seccion')
    list_seccion = cur.fetchall()
    cur.close()

    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from estante')
    list_estante = cur.fetchall()
    cur.close()
    return render_template('productos.html', user=current_user, list_productos = list_productos, list_unidad_medida= list_unidad_medida, list_tipo_impuesto = list_tipo_impuesto,
                            list_familia = list_familia, list_seccion = list_seccion, list_estante = list_estante, access=access, empresa=empresa)

@views.route('/agregar_producto', methods=['POST', 'GET'])
def agregarProducto():
    Producto.agregar_producto(request.method,request.form)
    return redirect(url_for('views.productos'))  

@views.route('/editar_producto', methods=['POST', 'GET'])
def editarProducto():
    Producto.editar_producto(request.method,request.form)
    return redirect(url_for('views.productos'))

@views.route('/eliminar_producto/<int:id>', methods=['POST', 'GET'])
def eliminarProducto(id):
    Producto.eliminar_producto(id)
    return redirect(url_for('views.productos'))

@views.route('/unidad_medida', methods=['GET', 'POST'])
def unidad_medida():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute("SELECT * from unidad_medida where tipo = 'C'")
    list_unidad_medida = cur.fetchall()
    cur.close()
    return render_template('unidad_medida.html', user=current_user, list_unidad_medida = list_unidad_medida, access = access, empresa = empresa)

@views.route('/agregar_unidad_medida', methods=['GET', 'POST'])
def agregarUnidadMedida():
    UnidadMedida.agregar_unidad_medida(request.method,request.form)
    return redirect(url_for('views.unidad_medida'))  

@views.route('/editar_unidad_medida', methods=['POST', 'GET'])
def editarUnidadMedida():
    UnidadMedida.editar_unidad_medida(request.method,request.form)
    return redirect(url_for('views.unidad_medida'))

@views.route('/tipo_impuesto', methods=['GET', 'POST'])
def tipo_impuesto():
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from tipo_impuesto')
    list_tipo_impuesto = cur.fetchall()
    cur.close()
    return render_template('productos.html', list_tipo_impuesto = list_tipo_impuesto)

@views.route('/familia', methods=['GET', 'POST'])
def familia():
    access = Access()
    empresa = Empresa()

    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from familia')
    list_familia = cur.fetchall()
    cur.close()
    return render_template('familia.html', user=current_user, list_familia = list_familia, access = access, empresa = empresa)

@views.route('/agregar_familia', methods=['POST', 'GET'])
def agregarFamilia():
    Familia.agregar_familia(request.method,request.form)
    return redirect(url_for('views.familia'))  

@views.route('/editar_familia', methods=['POST', 'GET'])
def editarFamilia():
    Familia.editar_familia(request.method,request.form)
    return redirect(url_for('views.familia'))

@views.route('/eliminar_familia/<int:id>', methods=['POST', 'GET'])
def eliminarFamilia(id):
    Familia.eliminar_familia(id)
    return redirect(url_for('views.familia'))

@views.route('/seccion', methods=['GET', 'POST'])
def seccion():
    access = Access()
    empresa = Empresa()

    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from seccion')
    list_seccion = cur.fetchall()
    cur.close()
    return render_template('seccion.html', user=current_user, list_seccion = list_seccion, access = access, empresa = empresa)

@views.route('/agregar_seccion', methods=['POST', 'GET'])
def agregarSeccion():
    Seccion.agregar_seccion(request.method,request.form)
    return redirect(url_for('views.seccion'))  

@views.route('/editar_seccion', methods=['POST', 'GET'])
def editarSeccion():
    Seccion.editar_seccion(request.method,request.form)
    return redirect(url_for('views.seccion'))

@views.route('/eliminar_seccion/<int:id>', methods=['POST', 'GET'])
def eliminarSeccion(id):
    Seccion.eliminar_seccion(id)
    return redirect(url_for('views.seccion'))

@views.route('/estante', methods=['GET', 'POST'])
def estante():
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from estante')
    list_estante = cur.fetchall()
    cur.close()
    return render_template('productos.html', list_estante = list_estante)

#-------------------------------Entrada de productos-------------------------------------------------
@views.route('/entrada', methods=['GET', 'POST'])
def entrada():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from entrada')
    list_entrada = cur.fetchall()
    cur.close()
    return render_template('entrada.html', user=current_user, list_entrada = list_entrada, access=access, empresa = empresa)

@views.route('/registrar_entrada', methods=['GET', 'POST'])
def registrarEntrada():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from productos')
    list_producto = cur.fetchall()
    cur.close()
    return render_template('registrar_entrada.html', user=current_user, list_producto=list_producto, access=access, empresa = empresa)

@views.route('/agregar_entrada', methods=['GET', 'POST'])
def agregarEntrada():
    access = Access()
    Entrada.agregar_entrada(request.method,request.form)
    return redirect(url_for('views.entrada'))  

@views.route('/select_entrada', methods=['GET', 'POST'])
def selectEntrada():   
    if request.method == 'POST': 
        id = request.form['entrada']
        cur = pool_db.getCursorSgp()
        result = cur.execute("SELECT * FROM entrada WHERE id = %s", [id])
        rsentrada = cur.fetchall()
        cur.close()
        entradaarray = []
        for rs in rsentrada:
            entrada_dict = {
                'nro_entrada': rs['nro_entrada'],
                'desc_entrada': rs['desc_entrada'],
                'fecha_entrada': rs['fecha_entrada']}
            entradaarray.append(entrada_dict)
        return json.dumps(entradaarray)
    
@views.route('/select_detalle_entrada', methods=['GET', 'POST'])
def selectDetalleEnt():   
    if request.method == 'POST': 
        id_entrada = request.form['entrada']
        cur = pool_db.getCursorSgp()
        result = cur.execute("""SELECT e.nro_entrada, d.cod_producto, d.cantidad, d.costo_unitario FROM detalle_entrada d join entrada e
                                on d.id_entrada = e.id
                                WHERE d.id_entrada = %s""", [id_entrada])
        rsdetalle = cur.fetchall()
        cur.close()
        detallearray = []
        for rs in rsdetalle:
            detalle_dict = {
                'numero': rs['nro_entrada'],
                'codigo': rs['cod_producto'],
                'cantidad': rs['cantidad'],
                'precio': rs['costo_unitario']}
            detallearray.append(detalle_dict)
        return json.dumps(detallearray)

@views.route('/carga_inventario', methods=['GET', 'POST'])
def cargaInventario():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from productos order by codigo')
    list_productos = cur.fetchall()
    cur.close()
    return render_template('carga_inventario.html', user=current_user, list_productos=list_productos, access=access, empresa = empresa)

@views.route('/agregar_carga', methods=['GET', 'POST'])
def agregarCarga():
    access = Access()
    Inventario.agregar_carga(request.method,request.form)
    return redirect(url_for('views.inventario'))

@views.route('/select_movimiento_detallado', methods=['GET', 'POST'])
def selectMovimientoDet():   
  if request.method == 'POST': 
    codigo = request.form['inventario']
    cur = pool_db.getCursorSgp()
    result = cur.execute("""(SELECT DE.cod_producto, DE.desc_producto, E.tipo_entrada tipo_movimiento, E.desc_entrada descripcion, to_char(E.fecha_entrada, 'DD/MM/YYYY') fecha, DE.cantidad FROM ENTRADA E
                             JOIN DETALLE_ENTRADA DE
                             ON E.id = DE.id_entrada
                             WHERE DE.cod_producto = %s
                             UNION						
                             SELECT P.codigo cod_producto, P.descripcion desc_producto, 'FC' tipo_movimiento, (select pr.name from proveedores pr where pr.ci_ruc = fc.proveedor_id) descripcion,  to_char(FC.fecha, 'DD/MM/YYYY') fecha, DC.cantidad  FROM factura_compra fc 
                             JOIN detalle_factura_compra DC 
                             ON DC.id_factura = FC.id_compra
                             JOIN PRODUCTOS P
                             ON DC.id_producto = P.id
                             WHERE DC.id_producto = (SELECT p.id FROM productos p where p.codigo = %s))
                             UNION
                             (SELECT DS.cod_producto, DS.desc_producto, S.tipo_salida tipo_movimiento, S.desc_salida descripcion, to_char(S.fecha_salida, 'DD/MM/YYYY') fecha, DS.cantidad*-1 FROM SALIDA S
                             JOIN DETALLE_SALIDA DS
                             ON S.id = DS.id_salida
                             WHERE DS.cod_producto = %s
                             UNION
                             SELECT P.codigo cod_producto, P.descripcion desc_producto, 'FV' tipo_movimiento, (select cl.name from clientes cl where cl.ci_ruc = f.cliente) descripcion, to_char(F.fecha, 'DD/MM/YYYY') fecha, DF.cantidad*-1  FROM factura F 
                             JOIN detalle_factura DF 
                             ON DF.id_factura = F.id
                             JOIN PRODUCTOS P
                             ON DF.id_producto = P.id
                             WHERE DF.id_producto = (SELECT p.id FROM productos p where p.codigo = %s))""", [codigo, codigo, codigo, codigo] )
    rsdetalle = cur.fetchall()
    cur.close()
    detallearray = []
    for rs in rsdetalle:
        detalle_dict = {
            'codigo': rs['cod_producto'],
            'producto': rs['desc_producto'],
            'tipo_movimiento': rs['tipo_movimiento'],
            'descripcion': rs['descripcion'],
            'fecha': rs['fecha'],
            'cantidad': rs['cantidad']}
        detallearray.append(detalle_dict)
    return json.dumps(detallearray)

@views.route('/selectproducto2', methods=['GET', 'POST'])
def selectproducto2():   
    if request.method == 'POST': 
        prod = request.form['prod']
        cur = pool_db.getCursorSgp()
        result = cur.execute("""select p.* from productos p
                    where p.codigo = %s""", [prod])
        rsproducto = cur.fetchall()
        cur.close()
        productoarray = []
        for rs in rsproducto:
            producto_dict = {
                'id': rs['id'],
                'precio1': rs['precio1'],
                'precio_promo': rs['precio_promo'],
                'precio_mayor': rs['precio_mayor'],
                'costo': rs['costo'],
                'cantidad': rs['cantidad'],
                'descripcion': rs['descripcion']}
            productoarray.append(producto_dict)
        return json.dumps(productoarray)

#-------------------------------Salida de productos-------------------------------------------------
@views.route('/salida', methods=['GET', 'POST'])
def salida():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from salida')
    list_salida= cur.fetchall()
    cur.close()
    return render_template('salida.html', user=current_user, list_salida = list_salida, access=access, empresa = empresa)

@views.route('/registrar_salida', methods=['GET', 'POST'])
def registrarSalida():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from productos')
    list_producto = cur.fetchall()
    cur.close()

    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * from entrada')
    list_entrada = cur.fetchall()
    cur.close()
    return render_template('registrar_salida.html', user=current_user, list_producto=list_producto, list_entrada = list_entrada, access=access, empresa = empresa)

@views.route('/agregar_salida', methods=['GET', 'POST'])
def agregarSalida():
    access = Access()
    Salida.agregar_salida(request.method,request.form)
    return redirect(url_for('views.salida')) 

@views.route('/select_detalle_salida', methods=['GET', 'POST'])
def selectDetalleSal():   
    if request.method == 'POST': 
        id_salida = request.form['salida']
        cur = pool_db.getCursorSgp()
        result = cur.execute("""SELECT s.nro_salida, d.cod_producto, d.cantidad, d.costo_unitario FROM detalle_salida d join salida s
                                on d.id_salida = s.id
                                WHERE d.id_salida = %s""", [id_salida])
        rsdetalle = cur.fetchall()
        cur.close()
        detallearray = []
        for rs in rsdetalle:
            detalle_dict = {
                'numero': rs['nro_salida'],
                'codigo': rs['cod_producto'],
                'cantidad': rs['cantidad'],
                'precio': rs['costo_unitario']}
            detallearray.append(detalle_dict)
        return json.dumps(detallearray)

@views.route('/inventario', methods=['GET', 'POST'])
def inventario():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM productos order by codigo')
    list_productos = cur.fetchall()
    cur.close()

    return render_template('inventario.html', user=current_user, list_productos=list_productos, access=access, empresa=empresa)

@views.route('/actualizar_producto/<string:codigo>/<float:cantidad_inventario>/', methods=['POST', 'GET'])
def actualizarProducto(codigo, cantidad_inventario):
    Inventario.actualizar_producto(codigo, cantidad_inventario)
    return redirect(url_for('views.inventario'))

@views.route('/listar_productos', methods=['GET', 'POST'])
def listarProductos():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM productos order by codigo')
    list_productos = cur.fetchall()
    cur.close()
    return render_template('listar_productos.html', user=current_user, list_productos=list_productos, access=access, empresa=empresa)

@views.route('/reporte_valorizado', methods=['GET', 'POST'])
def reporteValorizado():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute('SELECT * FROM productos order by codigo')
    list_productos = cur.fetchall()
    cur.close()
    return render_template('reporte_valorizado.html', user=current_user, list_productos=list_productos, access=access, empresa=empresa)

#-------------------------------Temporales-------------------------------------------------

@views.route('/nosotros', methods=['POST', 'GET'])
def nosotros():
    access = Access()
    empresa = Empresa()
    return render_template('nosotros.html',user=current_user, access=access, empresa=empresa)

@views.route('/pruebas', methods=['GET', 'POST'])
def pruebas():
    access = Access()
    empresa = Empresa()
    return render_template('pruebas.html', user=current_user, access=access, empresa=empresa)

@views.route('/vacio', methods=['POST','GET'])
def vacio():
    access = Access()
    empresa = Empresa()
    return render_template('vacio.html',user=current_user, access=access, empresa=empresa)

#-------------------------------Debug-------------------------------------------------

# Función que permite imprimir en el log con el método {{mdebug()}} en los templates HTML
@views.context_processor
def utility_functions():
    def print_in_console(message):
        print(message)

    return dict(mdebug=print_in_console)

@views.route('/promocion', methods=['POST','GET'])
def promocion():
    access = Access()
    empresa = Empresa()
    cur = pool_db.getCursorSgp()
    cur.execute("SELECT * FROM productos where descripcion not like '%Combo%'")
    list_productos = cur.fetchall()
    cur.close()
    return render_template('promocion.html',user=current_user, access=access, empresa=empresa, list_productos=list_productos)

@views.route('/crear_promocion', methods=['POST','GET'])
def crearPromocion():
    fecha_inicio = request.form['fecha-inicio']
    fecha_fin = request.form['fecha-fin']
    codigo = request.form['codigo']
    cantidad = request.form['cantidad']
    producto1 = request.form['prod1']
    producto2 = request.form['prod2']
    precio_promo = request.form['prec1']
    precio_promo2 = request.form['prec2']
    cantidad1 = int(request.form['cant1'])
    cantidad2 = int(request.form['cant2'])
    cur = pool_db.getCursorSgp()
    cur.execute("INSERT INTO promocion (fecha_inicio, fecha_fin, codigo, producto1, producto2,cantidad1,cantidad2,cantidad) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(fecha_inicio, fecha_fin, codigo, producto1, producto2,cantidad1,cantidad2,cantidad,))
    cur.connection.commit()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute("UPDATE productos set cantidad = cantidad - %s where codigo = %s",(int(cantidad)*int(cantidad1),producto1))
    cur.connection.commit()
    cur.close()
    cur = pool_db.getCursorSgp()
    cur.execute("UPDATE productos set cantidad = cantidad - %s where codigo = %s",(int(cantidad)*int(cantidad2),producto2))
    cur.connection.commit()
    cur.close()
    pre = int(precio_promo)*cantidad1 + int(precio_promo2)*cantidad2
    cur = pool_db.getCursorSgp()
    cur.execute("INSERT INTO productos (codigo, descripcion, precio1, tipo_impuesto, cantidad) VALUES (%s,%s,%s,%s,%s)", (codigo,'Combo ' + producto1 + ' + ' +producto2, pre,1,cantidad,))
    cur.connection.commit()
    cur.close()
    flash("Promoción Creada")
    return redirect(url_for('views.home'))

@views.route('/retirar_monto', methods=['POST','GET'])
def retirarDinero():
    empresa = Empresa()
    dinero = request.form['retirar-monto']
    cur = pool_db.getCursorSgp()
    cur.execute("UPDATE caja SET monto_actual = monto_actual - %s where nro_caja = %s", (dinero, empresa[11][0],))
    cur.connection.commit()
    cur.close()
    flash("Retiro Registrado")
    return redirect(url_for('views.caja'))