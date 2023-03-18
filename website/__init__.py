from os import path

import sqlalchemy as db
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists
from werkzeug.security import generate_password_hash

from website.database import db_config, pool_db

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abcd'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:12345@18.133.252.155:5432/postgres'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:12345@localhost/SYSPDV'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    
    from .auth import auth
    from .views import views

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Users


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    create_database(app)
    
    return app


def create_database(app):
    if not database_exists('postgresql://postgres@localhost/{db_config.DB_NAME}'):
        db.create_all(app=app)
        create_admin_permission()
        create_admin_rol()
        create_admin_user()
        create_tipo_documento()
        create_estado_cliente()
        create_unidad_medida()
        create_tipo_impuesto()
        create_familia()
        create_seccion()
        create_estante()
        create_empresa()
        print('Created Database!')    

def create_admin_user():
    cursor = pool_db.getCursorSgp()
    cursor.execute("SELECT EMAIL FROM USERS")
    account = cursor.fetchone()
    cursor.close()
    if not account:
        _hashed_password = generate_password_hash('admin')
        cursor = pool_db.getCursorSgp()
        cursor.execute("INSERT INTO users (email, password, name, rol_id) VALUES (%s,%s,%s,%s)", ('admin@gmail.com', _hashed_password, 'Admin', 1))
        cursor.connection.commit()
        cursor.close()

def create_admin_rol():
    cursor = pool_db.getCursorSgp()
    cursor.execute("SELECT id FROM rol")
    role = cursor.fetchone()
    cursor.close()
    if not role:
        cursor = pool_db.getCursorSgp()
        cursor.execute("INSERT INTO rol (rol_name) VALUES (%s)", ('Administrador',))
        cursor.connection.commit()
        cursor.close()
        cursor = pool_db.getCursorSgp()
        cursor.execute("INSERT INTO rol_permisos (id_rol, id_permisos) values (%s,%s)", (1,2,))
        cursor.execute("INSERT INTO rol_permisos (id_rol, id_permisos) values (%s,%s)", (1,3,))
        cursor.execute("INSERT INTO rol_permisos (id_rol, id_permisos) values (%s,%s)", (1,4,))
        cursor.execute("INSERT INTO rol_permisos (id_rol, id_permisos) values (%s,%s)", (1,5,))
        cursor.connection.commit()
        cursor.close()

def create_admin_permission():
    cursor = pool_db.getCursorSgp()
    cursor.execute("SELECT id FROM permiso")
    permiso = cursor.fetchone()
    cursor.close()
    if not permiso:
        cursor = pool_db.getCursorSgp()
        cursor.execute("INSERT INTO permiso (permisos, menu_padre, es_menu) VALUES (%s,%s,%s)", ('SYSPDV',0,True,))
        cursor.execute("INSERT INTO permiso (permisos, es_menu, menu_padre) values (%s,%s,%s)", ('Venta', True, 1,))
        cursor.execute("INSERT INTO permiso (permisos, es_menu, menu_padre) values (%s,%s,%s)", ('Compra', True, 1,))
        cursor.execute("INSERT INTO permiso (permisos, es_menu, menu_padre) values (%s,%s,%s)", ('Cuenta Corriente', True, 1,))
        cursor.execute("INSERT INTO permiso (permisos, es_menu, menu_padre) values (%s,%s,%s)", ('Stock', True, 1,))
        cursor.connection.commit()
        cursor.close()

##Tabla en la cual se cargan los tipos de documentos a elegir en el momento de crear un cliente
def create_tipo_documento():
    cursor = pool_db.getCursorSgp()
    cursor.execute("SELECT id FROM tipo_documento")
    tipo_doc = cursor.fetchone()
    cursor.close()
    if not tipo_doc:
        cursor = pool_db.getCursorSgp()
        cursor.execute("INSERT INTO tipo_documento (desc_tipo) VALUES (%s)", ('CI',))
        cursor.execute("INSERT INTO tipo_documento (desc_tipo) VALUES (%s)", ('RUC',))
        cursor.execute("INSERT INTO tipo_documento (desc_tipo) VALUES (%s)", ('CRC',))
        cursor.connection.commit()
        cursor.close()

##Tabla en la cual se cargan los estados que puede tener un cliente
def create_estado_cliente():
    cursor = pool_db.getCursorSgp()
    cursor.execute("SELECT id FROM estado_cliente")
    estado = cursor.fetchone()
    cursor.close()
    if not estado:
        cursor = pool_db.getCursorSgp()
        cursor.execute("INSERT INTO estado_cliente (desc_estado) VALUES (%s)", ('Activo',))
        cursor.execute("INSERT INTO estado_cliente (desc_estado) VALUES (%s)", ('Inactivo',))
        cursor.connection.commit()
        cursor.close()
##Tabla en la cual se cargan las unidades de medidas para los productos
def create_unidad_medida():
    cursor = pool_db.getCursorSgp()
    cursor.execute("SELECT id FROM unidad_medida")
    unidad_medida = cursor.fetchone()
    cursor.close()
    if not unidad_medida:
        cursor = pool_db.getCursorSgp()
        cursor.execute("INSERT INTO unidad_medida (desc_unidad_medida, tipo) VALUES (%s, %s)", ('Unidad', 'V',))
        cursor.execute("INSERT INTO unidad_medida (desc_unidad_medida, tipo) VALUES (%s, %s)", ('Kilogramo', 'V',))
        cursor.execute("INSERT INTO unidad_medida (desc_unidad_medida, tipo) VALUES (%s, %s)", ('Litro', 'V',))
        cursor.execute("INSERT INTO unidad_medida (desc_unidad_medida, tipo) VALUES (%s, %s)", ('Metro', 'V',))
        cursor.execute("INSERT INTO unidad_medida (desc_unidad_medida, tipo) VALUES (%s, %s)", ('M²', 'V',))
        cursor.connection.commit()
        cursor.close()

##Tabla en la cual se cargan los tipos de impuestos que pueden tener los productos
def create_tipo_impuesto():
    cursor = pool_db.getCursorSgp()
    cursor.execute("SELECT id FROM tipo_impuesto")
    tipo_impuesto = cursor.fetchone()
    cursor.close()
    if not tipo_impuesto:
        cursor = pool_db.getCursorSgp()
        cursor.execute("INSERT INTO tipo_impuesto (desc_tipo_impuesto) VALUES (%s)", ('10%',))
        cursor.execute("INSERT INTO tipo_impuesto (desc_tipo_impuesto) VALUES (%s)", ('05%',))
        cursor.execute("INSERT INTO tipo_impuesto (desc_tipo_impuesto) VALUES (%s)", ('Exentas',))
        cursor.connection.commit()
        cursor.close()
##Se carga de forma predeterminada los valores de N/A para familia
def create_familia():
    cursor = pool_db.getCursorSgp()
    cursor.execute("SELECT id FROM familia")
    familia = cursor.fetchone()
    cursor.close()
    if not familia:
        cursor = pool_db.getCursorSgp()
        cursor.execute("INSERT INTO familia (codigo, desc_familia) VALUES (%s, %s)", ('999', 'N/A',))
        cursor.connection.commit()
        cursor.close()
##Se carga de forma predeterminada los valores de N/A para grupo
def create_seccion():
    cursor = pool_db.getCursorSgp()
    cursor.execute("SELECT id FROM seccion")
    seccion = cursor.fetchone()
    cursor.close()
    if not seccion:
        cursor = pool_db.getCursorSgp()
        cursor.execute("INSERT INTO seccion (desc_seccion) VALUES (%s)", ('N/A',))
        cursor.connection.commit()
        cursor.close()

##Se carga de forma predeterminada los valores de N/A para grupo
def create_estante():
    cursor = pool_db.getCursorSgp()
    cursor.execute("SELECT id FROM estante")
    estante = cursor.fetchone()
    cursor.close()
    if not estante:
        cursor = pool_db.getCursorSgp()
        cursor.execute("INSERT INTO estante (desc_estante) VALUES (%s)", ('001',))
        cursor.execute("INSERT INTO estante (desc_estante) VALUES (%s)", ('002',))
        cursor.execute("INSERT INTO estante (desc_estante) VALUES (%s)", ('003',))
        cursor.execute("INSERT INTO estante (desc_estante) VALUES (%s)", ('004',))
        cursor.execute("INSERT INTO estante (desc_estante) VALUES (%s)", ('005',))
        cursor.connection.commit()
        cursor.close()

# Carga de datos predeterminados de la empresa
def create_empresa():
    cursor = pool_db.getCursorSgp()
    cursor.execute("SELECT id FROM empresa")
    empresa = cursor.fetchone()
    cursor.close()
    if not empresa:
        cursor = pool_db.getCursorSgp()
        cursor.execute("INSERT INTO empresa (direccion, eslogan, telefono, timbrado, nro_factura) VALUES (%s,%s,%s,%s,%s)", ('Calle yyyyyy C/ ejemplo', 'Dios es amor','(021)94x-xxx','23423423',1000000))
        cursor.connection.commit()
        cursor.close()