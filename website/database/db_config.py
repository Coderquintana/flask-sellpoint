#parametros para base de datos de sgp
DB_HOST = "localhost"
DB_NAME = "SYSPDV"
DB_USER = "postgres"
DB_PASS = "12345"

#parametros para base de datos de sgp
# DB_HOST = "18.133.252.155"
# DB_NAME = "postgres"
# DB_USER = "postgres"
# DB_PASS = "12345"

# (query que genera la columna de niveles de acceso)
# WITH RECURSIVE cte AS (
# 	SELECT id, menu_padre, permisos, 1 as lvl
# 	FROM permiso
# 	WHERE menu_padre is null
# 	UNION ALL
# 	SELECT p.id, p.menu_padre, p.permisos, c.lvl+1
# 	FROM permiso p
# 	JOIN cte c ON c.id = p.menu_padre )
# SELECT id, menu_padre, permisos, lvl FROM cte;

# (query para borrar todas las tablas)
# DROP TABLE detalle_pagos;
# DROP TABLE detalle_orden_compra;
# DROP TABLE detalle_factura_compra;
# DROP TABLE detalle_salida;
# DROP TABLE detalle_cobros;
# DROP TABLE detalle_entrada;
# DROP TABLE promocion;
# DROP TABLE cobros;
# DROP TABLE salida;
# DROP TABLE entrada;
# DROP TABLE rol_permisos;
# DROP TABLE user_permisos;
# DROP TABLE users;
# DROP TABLE clientes;
# DROP TABLE estado_cliente;
# DROP TABLE permiso;	
# DROP TABLE proveedores;
# DROP TABLE rol;
# DROP TABLE tipo_documento;
# DROP TABLE detalle_pedido;
# DROP TABLE pedido;
# DROP TABLE detalle_factura;
# DROP TABLE factura;
# DROP TABLE caja;
# DROP TABLE grupo;
# DROP TABLE tipo_impuesto;
# DROP TABLE unidad_medida;
# DROP TABLE familia;
# DROP TABLE empresa;
# DROP TABLE estado_pedido;
# DROP TABLE productos;
# DROP TABLE estante;
# DROP TABLE seccion;
# DROP TABLE orden_compra;
# DROP TABLE pagos;
# DROP TABLE factura_compra;

# --- PROCEDIMIENTOS PROCEDIMIENTOS ---#
#------------------------------------------------------------------------------------
# CREATE OR REPLACE PROCEDURE public.anular_factura(
# 	IN n_factura character varying)
# LANGUAGE 'plpgsql'
# AS $BODY$
# DECLARE
# 	c_producto CURSOR FOR 
# 		select * from detalle_factura 
# 		where id_factura = (select id from factura where nro_factura = n_factura);
# BEGIN
# 	FOR reg IN c_producto LOOP 
# 		UPDATE productos SET cantidad = cantidad + reg.cantidad
# 		where id = reg.id_producto;
# 	END LOOP;
	
# 	UPDATE public.factura SET anulado = true
# 	WHERE nro_factura = n_factura;
# END;
# $BODY$;
#------------------------------------------------------------------------------------
# CREATE OR REPLACE PROCEDURE public.aumentar_monto_actual(
# 	IN n_caja integer,
# 	IN monto_factura integer)
# LANGUAGE 'plpgsql'
# AS $BODY$
# DECLARE
# BEGIN
# 	UPDATE public.caja SET monto_actual = monto_actual + monto_factura
# 	WHERE nro_caja = n_caja;
# END;
# $BODY$;
#------------------------------------------------------------------------------------
# CREATE OR REPLACE PROCEDURE public.descontar_stock(
# 	IN p_producto integer,
# 	IN c_cantidad integer)
# LANGUAGE 'plpgsql'
# AS $BODY$
# BEGIN
# 	UPDATE public.productos SET cantidad = cantidad - c_cantidad
# 	WHERE id = p_producto;
# END;
# $BODY$;