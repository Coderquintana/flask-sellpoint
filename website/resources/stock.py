import datetime
from pickle import NONE

from flask import flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash

from website.database import pool_db
from website.models import productos


class Producto():
    def agregar_producto(rm,rf):
        if rm == 'POST' and 'codigo' in rf and 'descripcion' in rf and 'unidad_medida_venta' in rf and 'unidad_medida_compra' in rf and 'tipo_impuesto' in rf and 'familia' in rf and 'seccion' in rf and 'estante' in rf and 'precio1' in rf:
            codigo = rf['codigo']
            descripcion = rf['descripcion']
            unidad_medida_venta = rf['unidad_medida_venta']
            unidad_medida_compra = rf['unidad_medida_compra']
            tipo_impuesto = rf['tipo_impuesto']
            familia = rf['familia']
            seccion = rf['seccion']
            estante = rf['estante']
            precio1 = rf['precio1']
            precio2 = rf['precio2']
            precio3 = rf['precio3']
            precio4 = rf['precio4']
            precio_promo = rf['precio_promo']
            precio_mayor = rf['precio_mayor']
            stock_minimo = rf['stock_minimo']
            stock_maximo = rf['stock_maximo']
            #Comprueba si ya se cargo un producto con el mismo código
            cursor = pool_db.getCursorSgp()
            cursor.execute('SELECT * FROM productos WHERE codigo = %s', (codigo,))
            verifica = cursor.fetchone()
            cursor.close()
            # Si encuentra emite en pantalla el siguiente mensaje
            if verifica:
                flash('Ya existe un producto con este codigo!')
            else:
                # se obtiene la descripción de la unidad de medida
                cursor = pool_db.getCursorSgp()
                cursor.execute('SELECT desc_unidad_medida FROM unidad_medida WHERE id = %s', (unidad_medida_venta,))
                unidad_medida_descv = cursor.fetchone()[0]
                cursor.close()
                 # se obtiene la descripción de la unidad de medida
                cursor = pool_db.getCursorSgp()
                cursor.execute('SELECT desc_unidad_medida FROM unidad_medida WHERE id = %s', (unidad_medida_compra,))
                unidad_medida_descc = cursor.fetchone()[0]
                cursor.close()
                 # se obtiene la descripción de la familia
                cursor = pool_db.getCursorSgp()
                cursor.execute('SELECT desc_familia from familia WHERE id = %s', (familia,))
                familia_desc = cursor.fetchone()[0]
                cursor.close()
                # se obtiene la descripción del grupo
                cursor = pool_db.getCursorSgp()
                cursor.execute('SELECT desc_seccion FROM seccion WHERE id = %s', (seccion,))
                seccion_desc = cursor.fetchone()[0]
                cursor.close()

                try:
                    cursor = pool_db.getCursorSgp()
                    # Si la cuenta no existe, se inserta en la base de datos
                    cursor.execute("INSERT INTO productos (codigo, descripcion, unidad_medida_venta, unidad_medida_compra, tipo_impuesto, familia, seccion, estante, precio1, precio2, precio3, precio4, precio_promo, precio_mayor, cantidad, stock_minimo, stock_maximo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (codigo, descripcion, unidad_medida_descv, unidad_medida_descc, tipo_impuesto, familia_desc, seccion_desc, estante, precio1, precio2, precio3, precio4, precio_promo, precio_mayor, 0, stock_minimo, stock_maximo,))
                    cursor.connection.commit()
                    cursor.close()
                    flash('Registro exitoso!')
                    return redirect(url_for('views.productos'))
                except:
                    flash('No se ha podido registrar el producto')
        elif rm == 'POST':
            # Si el formulario esta vacio...
            flash('Por favor, complete el formulario!')
        return redirect(url_for('views.productos'))

    def editar_producto(rm,rf):
        if rm == 'POST' and 'id' in rf and 'descripcion' in rf and 'unidad_medida_venta' in rf and 'unidad_medida_compra' in rf and 'tipo_impuesto' in rf and 'familia' in rf and 'seccion' in rf and 'estante' in rf and 'precio1' in rf:
            id = rf['id']
            descripcion = rf['descripcion']
            unidad_medida_venta = rf['unidad_medida_venta']
            unidad_medida_compra = rf['unidad_medida_compra']
            tipo_impuesto = rf['tipo_impuesto']
            familia = rf['familia']
            seccion = rf['seccion']
            estante = rf['estante']
            precio1 = rf['precio1']
            precio2 = rf['precio2']
            precio3 = rf['precio3']
            precio4 = rf['precio4']
            precio_promo = rf['precio_promo']
            precio_mayor = rf['precio_mayor']
            stock_minimo = rf['stock_minimo']
            stock_maximo = rf['stock_maximo']

            # se obtiene la descripción de la unidad de medida
            cursor = pool_db.getCursorSgp()
            cursor.execute('SELECT desc_unidad_medida FROM unidad_medida WHERE id = %s', (unidad_medida_venta,))
            unidad_medida_descv = cursor.fetchone()[0]
            cursor.close()
            # se obtiene la descripción de la unidad de medida
            cursor = pool_db.getCursorSgp()
            cursor.execute('SELECT desc_unidad_medida FROM unidad_medida WHERE id = %s', (unidad_medida_compra,))
            unidad_medida_descc = cursor.fetchone()[0]
            cursor.close()
                # se obtiene la descripción de la familia
            cursor = pool_db.getCursorSgp()
            cursor.execute('SELECT desc_familia from familia WHERE id = %s', (familia,))
            familia_desc = cursor.fetchone()[0]
            cursor.close()
            # se obtiene la descripción del grupo
            cursor = pool_db.getCursorSgp()
            cursor.execute('SELECT desc_seccion FROM seccion WHERE id = %s', (seccion,))
            seccion_desc = cursor.fetchone()[0]
            cursor.close()

            try:
                cursor = pool_db.getCursorSgp()
                cursor.execute("UPDATE productos SET descripcion=%s, unidad_medida_venta=%s, unidad_medida_compra=%s, tipo_impuesto=%s, familia=%s, seccion=%s, estante=%s, precio1=%s, precio2=%s, precio3=%s, precio4=%s, precio_promo=%s, precio_mayor=%s, stock_minimo=%s, stock_maximo=%s WHERE id=%s", (descripcion, unidad_medida_descv, unidad_medida_descc, tipo_impuesto, familia_desc, seccion_desc, estante, precio1, precio2, precio3, precio4, precio_promo, precio_mayor, stock_minimo, stock_maximo, id, ))
                cursor.connection.commit()
                cursor.close()
                flash('Producto Modificado Correctamente!')
            except:
                flash('No se ha podido modificar el producto')

    def eliminar_producto(id):
      cursor = pool_db.getCursorSgp()
      cursor.execute('SELECT cantidad FROM productos WHERE id = %s', (id,))
      cantidad = cursor.fetchone()[0]
      cursor.close()

      if cantidad > 0:
        flash('No se puede eliminar esta Producto ya que posee stock')
      else:
        try:
          #se elimina de la tabla
          cur = pool_db.getCursorSgp()
          cur.execute('DELETE FROM productos WHERE id = {0}'.format(id))
          cur.connection.commit()
          cur.close()
          flash('Producto eliminado correctamente')
        except:
          flash('No se ha podido completar la operacion') 

class Entrada():
    def agregar_entrada(rm,rf):
        nro_entrada = rf['nro_entrada']
        desc_entrada = rf['desc_entrada']
        fecha_entrada = rf['fecha_entrada']
        costo_total = rf['monto_total']
         #Comprueba si el numero de entrada ya existe
        cursor = pool_db.getCursorSgp()
        cursor.execute('SELECT * FROM entrada WHERE nro_entrada = %s', (nro_entrada,))
        entrada = cursor.fetchone()
        cursor.close()

        if entrada:
           flash('Ya existe este número de entrada, favor verificar!')
        else:
            cursor = pool_db.getCursorSgp()
            cursor.execute("INSERT INTO entrada (nro_entrada, desc_entrada, tipo_entrada, costo_total, fecha_entrada ) VALUES (%s,%s,%s,%s,%s)",(nro_entrada, desc_entrada, 'ENT', costo_total,  fecha_entrada,))
            cursor.connection.commit()
            cursor.close()
        #se obtiene el id de la cabecera recien insertada
            cursor = pool_db.getCursorSgp()
            cursor.execute('SELECT max(id) FROM entrada WHERE nro_entrada = %s', (nro_entrada,))
            id_entrada = cursor.fetchone()[0]
            cursor.close()

            cantidad = 0
            costo = 0
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

                    cursor = pool_db.getCursorSgp()
                    cursor.execute('SELECT codigo FROM productos WHERE codigo = %s', (request.form[input],))
                    cod_producto = cursor.fetchone()[0]
                    cursor.close()

                    cursor = pool_db.getCursorSgp()
                    cursor.execute('SELECT coalesce(cantidad, 0) FROM productos WHERE codigo = %s', (request.form[input],))
                    cantidad_ant = cursor.fetchone()[0]
                    cursor.close()

                    cursor = pool_db.getCursorSgp()
                    cursor.execute('SELECT descripcion FROM productos WHERE codigo = %s', (request.form[input],))
                    descripcion = cursor.fetchone()[0]
                    cursor.close()

                    cursor = pool_db.getCursorSgp()
                    cursor.execute('SELECT unidad_medida_venta FROM productos WHERE codigo = %s', (request.form[input],))
                    unidad_med_venta = cursor.fetchone()[0]
                    cursor.close()

                    cursor = pool_db.getCursorSgp()
                    cursor.execute('SELECT coalesce(cantidad, 0)*coalesce(costo, 0) FROM productos WHERE codigo = %s', (request.form[input],))
                    costo_ant = cursor.fetchone()[0]
                    cursor.close()

                    cantidad_total = cantidad_ant + float(cantidad)

                elif 'costoR' in input:
                    costo = request.form[input]
                #calculo del costo promedio
                    costo_promedio = (costo_ant + (float(cantidad)*float(costo)))/cantidad_total

                if cantidad != 0 and producto != 0 and costo !=0 :
                    cursor = pool_db.getCursorSgp()
                    cursor.execute("INSERT INTO detalle_entrada (id_entrada, cod_producto, desc_producto, unidad_medida, costo_unitario, costo_promedio, cantidad) VALUES (%s,%s,%s,%s,%s,%s,%s)",(id_entrada, cod_producto, descripcion, unidad_med_venta, costo, costo_promedio, cantidad,))
                    cursor.connection.commit()
                    cursor.close()

                    cursor = pool_db.getCursorSgp()
                    cursor.execute("UPDATE productos SET costo=%s, costo_promedio=%s, cantidad=%s, ultima_fecha_carga=%s WHERE codigo=%s", (costo, costo_promedio, cantidad_total, fecha_entrada, cod_producto, ))
                    cursor.connection.commit()
                    cursor.close()

                    cantidad = 0
                    costo = 0
                    producto = 0

                    flash('Agregado Correctamente')

class Salida:
    def agregar_salida(rm,rf):
        nro_salida = rf['nro_salida']
        desc_salida = rf['desc_salida']
        fecha_salida = rf['fecha_salida']
        costo_total = rf['monto_total']
         #Comprueba si el numero de entrada ya existe
        cursor = pool_db.getCursorSgp()
        cursor.execute('SELECT * FROM salida WHERE nro_salida = %s', (nro_salida,))
        salida = cursor.fetchone()
        cursor.close()

        if salida:
           flash('Ya existe este número de salida, favor verificar!')
        else:
            cursor = pool_db.getCursorSgp()
            cursor.execute("INSERT INTO salida (nro_salida, desc_salida, tipo_salida, costo_total, fecha_salida ) VALUES (%s,%s,%s,%s,%s)",(nro_salida, desc_salida, 'SAL', costo_total,  fecha_salida,))
            cursor.connection.commit()
            cursor.close()
        #se obtiene el id de la cabecera recien insertada
            cursor = pool_db.getCursorSgp()
            cursor.execute('SELECT max(id) FROM salida WHERE nro_salida = %s', (nro_salida,))
            id_salida = cursor.fetchone()[0]
            cursor.close()

            cantidad = 0
            costo = 0
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

                    cursor = pool_db.getCursorSgp()
                    cursor.execute('SELECT codigo FROM productos WHERE codigo = %s', (request.form[input],))
                    cod_producto = cursor.fetchone()[0]
                    cursor.close()

                    cursor = pool_db.getCursorSgp()
                    cursor.execute('SELECT descripcion FROM productos WHERE codigo = %s', (request.form[input],))
                    descripcion = cursor.fetchone()[0]
                    cursor.close()

                    cursor = pool_db.getCursorSgp()
                    cursor.execute('SELECT unidad_medida_venta FROM productos WHERE codigo = %s', (request.form[input],))
                    unidad_med_venta = cursor.fetchone()[0]
                    cursor.close()

                    cursor = pool_db.getCursorSgp()
                    cursor.execute('SELECT coalesce(cantidad, 0) FROM productos WHERE codigo = %s', (request.form[input],))
                    cantidad_ant = cursor.fetchone()[0]
                    cursor.close()

                    cursor = pool_db.getCursorSgp()
                    cursor.execute('SELECT coalesce(cantidad, 0)*coalesce(costo, 0) FROM productos WHERE codigo = %s', (request.form[input],))
                    costo_ant = cursor.fetchone()[0]
                    cursor.close()

                    cantidad_total = cantidad_ant - float(cantidad)

                elif 'costoR' in input:
                    costo = request.form[input]
                #calculo del costo promedio
                    costo_promedio = (costo_ant - (float(cantidad)*float(costo)))/cantidad_total

                if cantidad != 0 and producto != 0 and costo !=0 :
                    cursor = pool_db.getCursorSgp()
                    cursor.execute("INSERT INTO detalle_salida (id_salida, cod_producto, desc_producto, unidad_medida, costo_unitario, costo_promedio, cantidad) VALUES (%s,%s,%s,%s,%s,%s,%s)",(id_salida, cod_producto, descripcion, unidad_med_venta, costo, costo_promedio, cantidad,))
                    cursor.connection.commit()
                    cursor.close()

                    cursor = pool_db.getCursorSgp()
                    cursor.execute("UPDATE productos SET costo=%s, costo_promedio=%s, cantidad=%s, ultima_fecha_carga=%s WHERE codigo=%s", (costo, costo_promedio, cantidad_total, fecha_salida, cod_producto, ))
                    cursor.connection.commit()
                    cursor.close()

                    cantidad = 0
                    costo = 0
                    producto = 0

                    flash('Agregado Correctamente')

class Familia():
  def agregar_familia(rm,rf):
    if rm == 'POST' and 'codigo' in rf and 'desc_familia' in rf:
      codigo = rf['codigo']
      descripcion = rf['desc_familia']
      #Comprueba si ya se cargo una familia con el mismo código
      cursor = pool_db.getCursorSgp()
      cursor.execute('SELECT * FROM familia WHERE codigo = %s', (codigo,))
      verifica = cursor.fetchone()
      cursor.close()
      # Si encuentra emite en pantalla el siguiente mensaje
      if verifica:
        flash('Ya existe familia con este codigo!')
      else:
        try:
          cursor = pool_db.getCursorSgp()
          # Si la cuenta no existe, se inserta en la base de datos
          cursor.execute("INSERT INTO familia (codigo, desc_familia) VALUES (%s,%s)", (codigo, descripcion,))
          cursor.connection.commit()
          cursor.close()
          flash('Registro exitoso!')
          return redirect(url_for('views.familia'))
        except:
          flash('No se ha podido registrar la familia')
    elif rm == 'POST':
        # Si el formulario esta vacio...
      flash('Por favor, complete el formulario!')
    return redirect(url_for('views.familia'))

  def editar_familia(rm,rf):
    if rm == 'POST' and 'id' in rf and 'codigo' in rf and 'desc_familia' in rf:
      id = rf['id']
      codigo = rf['codigo']
      descripcion = rf['desc_familia']

      cursor = pool_db.getCursorSgp()
      cursor.execute('SELECT desc_familia FROM familia WHERE id = %s', (id,))
      familia_ant = cursor.fetchone()[0]
      cursor.close()

      try:
        cursor = pool_db.getCursorSgp()
        cursor.execute("UPDATE familia SET codigo=%s, desc_familia=%s WHERE id=%s", (codigo, descripcion, id, ))
        cursor.connection.commit()
        cursor.close()

        cursor = pool_db.getCursorSgp()
        cursor.execute("UPDATE productos SET familia=%s WHERE familia=%s", (descripcion, familia_ant, ))
        cursor.connection.commit()
        cursor.close()

        flash('Familia Modificada Correctamente!')
      except:
        flash('No se ha podido modificar la familia')

  def eliminar_familia(id):
    cursor = pool_db.getCursorSgp()
    cursor.execute('SELECT desc_familia FROM familia WHERE id = %s', (id,))
    verifica = cursor.fetchone()[0]
    cursor.close()

    if verifica == 'N/A':
      flash('No se puede eliminar esta Familia')
    else:
      try:
        #se elimina de la tabla
        cur = pool_db.getCursorSgp()
        cur.execute('DELETE FROM familia WHERE id = {0}'.format(id))
        cur.connection.commit()
        cur.close()
        #se elimina de los productos que lo tenian seleccionado
        cursor = pool_db.getCursorSgp()
        cursor.execute("UPDATE productos SET familia=%s WHERE familia=%s", ("", verifica, ))
        cursor.connection.commit()
        cursor.close()

        flash('Familia eliminada correctamente')
      except:
        flash('No se ha podido completar la operacion') 
        
class UnidadMedida():
  def agregar_unidad_medida(rm,rf):
    if rm == 'POST' and 'desc_unidad_medida' in rf and 'cantidad' in rf:
      descripcion = rf['desc_unidad_medida']
      cantidad = rf['cantidad']
      tipo = 'C'
      try:
        cursor = pool_db.getCursorSgp()
        # Si la cuenta no existe, se inserta en la base de datos
        cursor.execute("INSERT INTO UNIDAD_MEDIDA (desc_unidad_medida, tipo, cantidad) VALUES (%s,%s,%s)", (descripcion, tipo, cantidad,))
        cursor.connection.commit()
        cursor.close()
        flash('Registro exitoso!')
        return redirect(url_for('views.unidad_medida'))
      except:
        flash('No se ha podido registrar la Unidad de Medida')
    elif rm == 'POST':
      # Si el formulario esta vacio...
      flash('Por favor, complete el formulario!')
    return redirect(url_for('views.unidad_medida'))

  def editar_unidad_medida(rm,rf):
    if rm == 'POST' and 'id' in rf and 'desc_unidad_medida' in rf and 'cantidad' in rf:
      id = rf['id']
      descripcion = rf['desc_unidad_medida']
      cantidad = rf['cantidad']

      try:
        cursor = pool_db.getCursorSgp()
        cursor.execute("UPDATE unidad_medida SET desc_unidad_medida=%s, cantidad=%s WHERE id=%s", (descripcion, cantidad, id, ))
        cursor.connection.commit()
        cursor.close()

        flash('Unidad de Medida Modificada Correctamente!')
      except:
        flash('No se ha podido modificar la Unidad de Medida')

class Seccion():
  def agregar_seccion(rm,rf):
    if rm == 'POST' and 'desc_seccion' in rf:
      descripcion = rf['desc_seccion']
      #Comprueba si ya se cargo una familia con el mismo código
      cursor = pool_db.getCursorSgp()
      cursor.execute('SELECT * FROM seccion WHERE desc_seccion = %s', (descripcion,))
      verifica = cursor.fetchone()
      cursor.close()
      # Si encuentra emite en pantalla el siguiente mensaje
      if verifica:
        flash('Ya existe esta sección!')
      else:
        try:
          cursor = pool_db.getCursorSgp()
          # Si la cuenta no existe, se inserta en la base de datos
          cursor.execute("INSERT INTO seccion (desc_seccion) VALUES (%s)", (descripcion,))
          cursor.connection.commit()
          cursor.close()
          flash('Registro exitoso!')
          return redirect(url_for('views.seccion'))
        except:
          flash('No se ha podido registrar la sección')
    elif rm == 'POST':
        # Si el formulario esta vacio...
      flash('Por favor, complete el formulario!')
    return redirect(url_for('views.seccion'))

  def editar_seccion(rm,rf):
    if rm == 'POST' and 'desc_familia' in rf:
      id = rf['id']
      descripcion = rf['desc_familia']

      cursor = pool_db.getCursorSgp()
      cursor.execute('SELECT desc_seccion FROM seccion WHERE id = %s', (id,))
      seccion_ant = cursor.fetchone()[0]
      cursor.close()

      try:
        cursor = pool_db.getCursorSgp()
        cursor.execute("UPDATE seccion SET desc_seccion=%s WHERE id=%s", (descripcion, id, ))
        cursor.connection.commit()
        cursor.close()

        if seccion_ant:
          cursor = pool_db.getCursorSgp()
          cursor.execute("UPDATE productos SET seccion=%s WHERE seccion=%s", (descripcion, seccion_ant, ))
          cursor.connection.commit()
          cursor.close()
          flash('Sección Modificada Correctamente!')
        else:
          cursor = pool_db.getCursorSgp()
          cursor.execute("UPDATE seccion SET desc_seccion=%s WHERE id=%s", (descripcion, id, ))
          cursor.connection.commit()
          cursor.close()
          flash('Sección Modificada Correctamente!')
      except:
        flash('No se ha podido modificar la sección')

  def eliminar_seccion(id):
    cursor = pool_db.getCursorSgp()
    cursor.execute('SELECT desc_seccion FROM seccion WHERE id = %s', (id,))
    verifica = cursor.fetchone()[0]
    cursor.close()

    if verifica == 'N/A':
      flash('No se puede eliminar esta Sección')
    else:
      try:
        #se elimina de la tabla
        cur = pool_db.getCursorSgp()
        cur.execute('DELETE FROM seccion WHERE id = {0}'.format(id))
        cur.connection.commit()
        cur.close()
        #se elimina de los productos que lo tenian seleccionado
        cursor = pool_db.getCursorSgp()
        cursor.execute("UPDATE productos SET seccion=%s WHERE seccion=%s", ("", verifica, ))
        cursor.connection.commit()
        cursor.close()

        flash('Sección eliminada correctamente')
      except:
        flash('No se ha podido completar la operacion') 

class Inventario():
  def agregar_carga(rm,rf):
      po_retorno = ""
      for input in request.form:
          if 'prod-' in input:
              codigo = input.split("-")[1]
              cantidad = request.form[input]

              if cantidad == '0':
                continue
              else:
                try:
                  cursor = pool_db.getCursorSgp()
                  cursor.execute("SELECT cantidad_inventario FROM productos where codigo=%s", (codigo, ))
                  verificar = cursor.fetchone()
                  cursor.close()
                  if verificar:
                    cursor = pool_db.getCursorSgp()
                    cursor.execute("UPDATE productos set cantidad_inventario=%s where codigo=%s", (cantidad, codigo, ))
                    cursor.connection.commit()
                    cursor.close()
                    po_retorno = "OK"
                except:
                  flash('No se ha podido completar la operacion')
      if po_retorno == "OK":
          flash('Se actualizo correctamente')

  def actualizar_producto(codigo, cantidad_inventario):
    cursor = pool_db.getCursorSgp()
    cursor.execute('SELECT * FROM productos WHERE codigo = %s', (codigo,))
    verifica = cursor.fetchone()
    cursor.close()
  #se obtiene la cantidad actual del producto
    cursor = pool_db.getCursorSgp()
    cursor.execute('SELECT cantidad FROM productos WHERE codigo = %s', (codigo,))
    cantidad_actual = cursor.fetchone()[0]
    cursor.close()
  #se obtiene la descripcion del producto
    cursor = pool_db.getCursorSgp()
    cursor.execute('SELECT descripcion  FROM productos WHERE codigo = %s', (codigo,))
    descripcion = cursor.fetchone()[0]
    cursor.close()

    cursor = pool_db.getCursorSgp()
    cursor.execute('SELECT unidad_medida_venta  FROM productos WHERE codigo = %s', (codigo,))
    unidad_medida = cursor.fetchone()[0]
    cursor.close()
    if verifica:
      try:
        #actualiza las tablas
        cur = pool_db.getCursorSgp()
        cur.execute('UPDATE productos set cantidad =%s, cantidad_inventario=%s WHERE codigo =%s', (cantidad_inventario, 0, codigo))
        cur.connection.commit()
        cur.close()

        if cantidad_actual < cantidad_inventario:
          #obtenemos el ultimo id de entrada
            cantidad_final = cantidad_inventario - cantidad_actual
            cursor = pool_db.getCursorSgp()
            cursor.execute('SELECT max(id) FROM entrada' )
            id_entrada = cursor.fetchone()[0]
            cursor.close()
          #obtenemos el nuevo numero de entrada
            cursor = pool_db.getCursorSgp()
            cursor.execute('SELECT nro_entrada + 1 FROM entrada where id = %s', (id_entrada,))
            nro_entrada = cursor.fetchone()[0]
            cursor.close()
          #inserta la cabecera de la entrada
            cursor = pool_db.getCursorSgp()
            cursor.execute("INSERT INTO entrada (nro_entrada, desc_entrada, tipo_entrada, costo_total ) VALUES (%s,%s,%s,%s)",(nro_entrada, 'Entrada por inventario', 'ENT', 0,))
            cursor.connection.commit()
            cursor.close()
        #se obtiene el id de la cabecera recien insertada
            cursor = pool_db.getCursorSgp()
            cursor.execute('SELECT max(id) FROM entrada WHERE nro_entrada = %s', (nro_entrada,))
            id_entrada_det = cursor.fetchone()[0]
            cursor.close()
        #se inserta el detalle de la entrada
            cursor = pool_db.getCursorSgp()
            cursor.execute("INSERT INTO detalle_entrada (id_entrada, cod_producto, desc_producto, unidad_medida, costo_unitario, costo_promedio, cantidad) VALUES (%s,%s,%s,%s,%s,%s,%s)",(id_entrada_det, codigo, descripcion, unidad_medida, 0, 0, cantidad_final,))
            cursor.connection.commit()
            cursor.close()
        
        if cantidad_actual > cantidad_inventario:
            #obtenemos el ultimo id de salida
            cantidad_final = cantidad_actual - cantidad_inventario
            cursor = pool_db.getCursorSgp()
            cursor.execute('SELECT max(id) FROM salida' )
            id_salida = cursor.fetchone()[0]
            cursor.close()
          #obtenemos el nuevo numero de entrada
            cursor = pool_db.getCursorSgp()
            cursor.execute('SELECT nro_salida + 1 FROM entrada where id = %s', (id_salida,))
            nro_salida = cursor.fetchone()[0]
            cursor.close()
          #se inserta la cabecera de la salida
            cursor = pool_db.getCursorSgp()
            cursor.execute("INSERT INTO salida (nro_salida, desc_salida, tipo_salida, costo_total ) VALUES (%s,%s,%s,%s)",(nro_salida, 'Salida por Inventario', 'SAL', 0, ))
            cursor.connection.commit()
            cursor.close()
          #se obtiene el id de la cabecera recien insertada
            cursor = pool_db.getCursorSgp()
            cursor.execute('SELECT max(id) FROM salida WHERE nro_salida = %s', (nro_salida,))
            id_salida_det = cursor.fetchone()[0]
            cursor.close()
          #se inserta el detalle de la salida
            cursor = pool_db.getCursorSgp()
            cursor.execute("INSERT INTO detalle_salida (id_salida, cod_producto, desc_producto, unidad_medida, costo_unitario, costo_promedio, cantidad) VALUES (%s,%s,%s,%s,%s,%s,%s)",(id_salida_det, codigo, descripcion, unidad_medida, 0, 0, cantidad_final,))
            cursor.connection.commit()
            cursor.close()

        flash('Stock actualizado correctamente')
      except:
        flash('No se ha podido completar la operacion')
    else:
      flash('El producto no existe!')




    