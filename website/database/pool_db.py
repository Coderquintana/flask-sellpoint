# Clase para crear cursores apuntando a la base de datos
import logging
import psycopg2
from . import db_config
import psycopg2.extras

def getCursorSgp():
    con = psycopg2.connect(dbname=db_config.DB_NAME, user=db_config.DB_USER, password=db_config.DB_PASS, host=db_config.DB_HOST)
    logging.debug("Conectada BD local")
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return cur