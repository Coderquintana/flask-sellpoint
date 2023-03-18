import functools
from datetime import datetime
from email.policy import default

from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db

# Clase SQLalchemy para la creación y relación de las tablas

#------------------------------Seguridad----------------------------------------------

class rol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rol_name = db.Column(db.String(50))
    creation_date = db.Column(db.DateTime, server_default=func.now(), nullable=False)

class permiso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    permisos = db.Column(db.String(350), unique=True)
    es_menu = db.Column(db.Boolean)
    menu_padre = db.Column(db.Integer)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    nick_name = db.Column(db.String(150))
    creation_date = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    end_date = db.Column(db.DateTime(timezone=True))
    date_birth = db.Column(db.DateTime())
    phone = db.Column(db.String(50), unique=True)
    ci = db.Column(db.Integer)
    city = db.Column(db.String(150))
    neighborhood = db.Column(db.String(150))
    age = db.Column(db.Integer)
    # age = db.Column(db.String(200), nullable=False, server_default=func.age(func.now(),date_birth))
    address = db.Column(db.String(500))
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'))

class rol_permisos(db.Model):
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id'), primary_key=True)
    id_permisos = db.Column(db.Integer, db.ForeignKey('permiso.id'), primary_key=True)
    read = db.Column(db.Boolean)
    write = db.Column(db.Boolean)
    delete = db.Column(db.Boolean)

class user_permisos(db.Model):
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    id_permisos = db.Column(db.Integer, db.ForeignKey('permiso.id'), primary_key=True)

#------------------------------Clientes----------------------------------------------

class clientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_documento = db.Column(db.Integer)
    ci_ruc = db.Column(db.String(20), unique = True)
    name = db.Column(db.String(150))
    address = db.Column(db.String(500))
    email = db.Column(db.String(150), unique=True)
    creation_date = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    phone = db.Column(db.String(50), unique=True)
    city = db.Column(db.String(150))
    cred_limite = db.Column(db.Integer)
    neighborhood = db.Column(db.String(150))
    estado = db.Column(db.Integer)
    
class tipo_documento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc_tipo = db.Column(db.String(50))

class estado_cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc_estado = db.Column(db.String(50))

class cobros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nro_recibo= db.Column(db.Integer)
    ci_ruc = db.Column(db.String(20), unique = True)
    name = db.Column(db.String(150))
    tipo_cobro = db.Column(db.String(50))
    total_cobrado = db.Column(db.Integer)
    total_efectivo = db.Column(db.Integer)
    total_transferencia = db.Column(db.Integer)
    total_tarjeta = db.Column(db.Integer)
    descripcion = db.Column(db.String(150))
    creation_date = db.Column(db.DateTime, server_default=func.now(), nullable=False)

class detalle_cobros(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('cobros.id'), primary_key=True)
    nro_factura= db.Column(db.String(50))
    total_factura = db.Column(db.Integer)
    total_cobrado_fac = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    pos = db.Column(db.String(20))
    nro_cuenta = db.Column(db.String(20))

#------------------------------Proveedores----------------------------------------------

class proveedores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_documento = db.Column(db.Integer)
    ci_ruc = db.Column(db.String(20), unique = True)
    name = db.Column(db.String(150))
    address = db.Column(db.String(500))
    email = db.Column(db.String(150), unique=True)
    creation_date = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    phone = db.Column(db.String(50), unique=True)
    city = db.Column(db.String(150))
    neighborhood = db.Column(db.String(150))

class pagos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nro_pago= db.Column(db.Integer)
    ci_ruc = db.Column(db.String(20))
    name = db.Column(db.String(150))
    tipo_pago = db.Column(db.String(150))
    total_factura = db.Column(db.Integer)
    saldo_factura = db.Column(db.Integer)
    total_pagado = db.Column(db.Integer)
    descripcion = db.Column(db.String(150))
    creation_date = db.Column(db.DateTime, server_default=func.now(), nullable=False)

class detalle_pagos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nro_factura = db.Column(db.String(20))
    total_factura = db.Column(db.Integer)
    total_pagado_fac = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime, server_default=func.now(), nullable=False)

#------------------------------Productos----------------------------------------------

#Tabla en la cual se cargan los productos
class productos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True)
    descripcion = db.Column(db.String(100))
    unidad_medida_venta = db.Column(db.String(50))
    unidad_medida_compra = db.Column(db.String(50))
    tipo_impuesto = db.Column(db.Integer)
    precio1 = db.Column(db.Integer)
    precio2 = db.Column(db.Integer)
    precio3 = db.Column(db.Integer)
    precio4 = db.Column(db.Integer)
    precio_promo = db.Column(db.Integer)
    precio_mayor = db.Column(db.Integer)
    costo = db.Column(db.Integer)
    costo_promedio = db.Column(db.Integer)
    cantidad = db.Column(db.Float)
    cantidad_inventario = db.Column(db.Float)
    familia = db.Column(db.String(50))
    seccion = db.Column(db.String(50))
    estante = db.Column(db.String(50))
    stock_minimo = db.Column(db.Integer)
    stock_maximo = db.Column(db.Integer)
    ultima_fecha_carga = db.Column(db.Date)
    fecha_creacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)

#Tabla en la cual se carga las unidades de medidas posibles para los productos
class unidad_medida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc_unidad_medida = db.Column(db.String(150))
    val_unidad = db.Column(db.Integer)
    tipo = db.Column(db.String(1))
    cantidad = db.Column(db.Float)

#Tabla en la cual se cargan los tipos de impuestos posibles para los productos
class tipo_impuesto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc_tipo_impuesto = db.Column(db.String(150))

class familia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(15))
    desc_familia = db.Column(db.String(150))

class seccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc_seccion = db.Column(db.String(150))

class estante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc_estante = db.Column(db.String(150))

class entrada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nro_entrada = db.Column(db.Integer)
    desc_entrada = db.Column(db.String(100))
    tipo_entrada = db.Column(db.String(3))
    costo_total = db.Column(db.Integer)
    fecha_entrada = db.Column(db.DateTime, server_default=func.now(), nullable=False)

class detalle_entrada(db.Model):
    id_entrada = db.Column(db.Integer, db.ForeignKey('entrada.id'), primary_key=True)
    cod_producto = db.Column(db.String(20), db.ForeignKey('productos.codigo'), primary_key=True)
    desc_producto = db.Column(db.String(100))
    unidad_medida = db.Column(db.String(50))
    costo_unitario = db.Column(db.Integer)
    costo_promedio = db.Column(db.Integer)
    cantidad = db.Column(db.Float)
    fecha_entrada = db.Column(db.DateTime, server_default=func.now(), nullable=False)

class salida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nro_salida = db.Column(db.Integer)
    desc_salida = db.Column(db.String(100))
    tipo_salida = db.Column(db.String(3))
    costo_total = db.Column(db.Integer)
    fecha_salida = db.Column(db.DateTime, server_default=func.now(), nullable=False)

class detalle_salida(db.Model):
    id_salida = db.Column(db.Integer, db.ForeignKey('salida.id'), primary_key=True)
    cod_producto = db.Column(db.String(20), db.ForeignKey('productos.codigo'), primary_key=True)
    desc_producto = db.Column(db.String(100))
    unidad_medida = db.Column(db.String(50))
    costo_unitario = db.Column(db.Integer)
    costo_promedio = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)
    fecha_salida = db.Column(db.DateTime, server_default=func.now(), nullable=False)

#------------------------------Venta----------------------------------------------
# Tabla de datos correspondiente a la caja
class caja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nro_caja = db.Column(db.Integer)
    fecha = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_cierre = db.Column(db.DateTime(timezone=True))
    monto_inicial = db.Column(db.Integer)
    monto_actual = db.Column(db.Integer)
    monto_cierre = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

# Tabla cabecera de las facturas
class factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nro_factura = db.Column(db.String)
    fecha = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    tipo_comprobante = db.Column(db.Integer)
    condicion_pago = db.Column(db.String(20))
    forma_pago = db.Column (db.String(20))
    monto_total = db.Column(db.Integer)
    pedido = db.Column(db.Boolean)
    pedido_id = db.Column(db.Integer)
    delivery_ci = db.Column(db.String(20))
    delivery_phone = db.Column(db.String(30))
    estado = db.Column(db.String(10))
    cliente = db.Column(db.String)
    nro_caja = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    anulado = db.Column(db.Boolean)
    pos = db.Column(db.String(20))
    nro_cuenta = db.Column(db.String(20))

# Tabla asociada a la cabecera con el detalle de las facturas
class detalle_factura(db.Model):
    id_factura = db.Column(db.Integer, db.ForeignKey('factura.id'), primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id'), primary_key=True)
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Integer)

# Tabla donde se guardan los pedidos con sus estados
class pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_registro = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    estado = db.Column(db.String(20))
    fecha_entrega = db.Column(db.Date)
    cliente_id = db.Column(db.String(20))
    user_id = db.Column(db.Integer)

# Tabla donde se detallan los pedidos
class detalle_pedido(db.Model):
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id'), primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id'), primary_key=True)
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Integer)

# Tabla de posibles estados del pedido
class estado_pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(50))
#------------------------------Compras----------------------------------------------
# Tabla cabecera de las facturas de compras
class factura_compra(db.Model):
    id_compra = db.Column(db.Integer, primary_key=True)
    nro_factura_compra = db.Column(db.String(20))
    timbrado = db.Column(db.String(20))
    fecha = db.Column(db.Date)
    condicion_pago = db.Column(db.String(20))
    monto_total = db.Column(db.Integer)
    saldo_factura = db.Column(db.Integer)
    ordencompra = db.Column(db.Integer)
    estado = db.Column(db.String(10))
    proveedor_id = db.Column(db.String(20))
    user_id = db.Column(db.Integer)

# Tabla asociada a la cabecera con el detalle de las facturas de compra
class detalle_factura_compra(db.Model):
    id_factura = db.Column(db.Integer, db.ForeignKey('factura_compra.id_compra'), primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id'), primary_key=True)
    cantidad = db.Column(db.Integer)
    unidad_medida = db.Column(db.String(40))
    precio = db.Column(db.Integer)

# Tabla donde se guardan las ordenes de compra con sus estados
class orden_compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_registro = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    descripcion = db.Column(db.String(150))
    estado = db.Column(db.String(10))
    fecha_pago = db.Column(db.Date)
    proveedor_id = db.Column(db.String(20))
    user_id = db.Column(db.Integer)
# Tabla donde se detallan las ordenes de compras
class detalle_orden_compra(db.Model):
    id_compra_det = db.Column(db.Integer, db.ForeignKey('orden_compra.id'), primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id'), primary_key=True)
    cantidad = db.Column(db.Integer)
    unidad_medida = db.Column(db.String(40))
    precio = db.Column(db.Integer)

#------------------------------Empresa----------------------------------------------
# Tabla que guarda los datos de la empresa para ver en la factura
class empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    direccion = db.Column(db.String(200))
    ciudad = db.Column(db.String(30))
    barrio = db.Column(db.String(30))
    eslogan = db.Column(db.String(200))
    telefono = db.Column(db.String(200))
    email = db.Column(db.String(40))
    timbrado = db.Column(db.String(30))
    nro_factura = db.Column(db.Integer)
    factura_inicio = db.Column(db.Integer)
    factura_fin = db.Column(db.Integer)
    
class promocion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_inicio = db.Column(db.DateTime)
    fecha_fin = db.Column(db.DateTime)
    codigo = db.Column(db.String(20))
    cantidad = db.Column(db.Integer)
    producto1 = db.Column(db.String(20))
    cantidad1 = db.Column(db.Integer)
    producto2 = db.Column(db.String(20))
    cantidad2 = db.Column(db.Integer)