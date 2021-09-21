from SalvandoAlimentos.data.data_base import BaseDeDatos


def obtener_usuario(id_usuario):
    obtener_usuarios_sql = f"""
        SELECT id, name, email, user_name 
        FROM users 
        WHERE id = {id_usuario}
    """
    bd = BaseDeDatos()
    return [{"id": row[0],
             "name": row[1],
             "email": row[2],
             "user_name": row[3]
             } for row in bd.ejecutar_sql(obtener_usuarios_sql)]


def obtener_usuarios():
    obtener_usuarios_sql = f"""
        SELECT id, name, email, user_name 
        FROM users
    """
    bd = BaseDeDatos()
    return [{"id": row[0],
             "name": row[1],
             "email": row[2],
             "user_name": row[3]
             } for row in bd.ejecutar_sql(obtener_usuarios_sql)]


def obtener_usuarios_por_nombre_clave(user_name, password):
    obtener_usuario_sql = f"""
            SELECT id, name, email 
            FROM users
            WHERE user_name='{user_name}' AND password='{password}'
        """
    bd = BaseDeDatos()
    return [{"id": row[0],
             "name": row[1],
             "email": row[2]
             } for row in bd.ejecutar_sql(obtener_usuario_sql)]


def crear_sesion(id_usuario, dt_string):
    crear_sesion_sql = f"""
               INSERT INTO sessions(id_user, date_time)
               VALUES ('{id_usuario}', '{dt_string}')
           """
    bd = BaseDeDatos()
    return bd.ejecutar_sql(crear_sesion_sql)


def obtener_sesion(id_sesion):
    obtener_sesion_sql = f"""
        SELECT id, id_user, date_time FROM sessions WHERE id = {id_sesion}
    """
    bd = BaseDeDatos()
    return [{"id": registro[0],
             "id_user": registro[1],
             "date_time": registro[2]}
            for registro in bd.ejecutar_sql(obtener_sesion_sql)]


def create_user(name, email, user_name, password, address):
    create_user_sql = f"""
        INSERT INTO users(name, email, user_name, password, address) 
        VALUES ('{name}', '{email}', '{user_name}', '{password}', '{address}') 
    """

    bd = BaseDeDatos()
    bd.ejecutar_sql(create_user_sql)


def update_user(id, name, password):
    update_user_sql = f"""
        UPDATE users SET name='{name}', password='{password}' 
        WHERE id={id}
    """

    bd = BaseDeDatos()
    bd.ejecutar_sql(update_user_sql)


def delete_user(id_user):
    delete_user_sql = f"""
        DELETE FROM users WHERE id={id_user}
    """
    bd = BaseDeDatos()
    bd.ejecutar_sql(delete_user_sql)



# def user_login(user_name, password):
#     user_login_sql = f"""
#         SELECT * FROM users WHERE user_name='{user_name}' AND password='{password}'
#     """
#     bd = BaseDeDatos()
#     bd._crear_conexion()
#     cursor = bd.conexion.cursor()
#     cursor.execute(user_login_sql)
#
#     query_result = [ dict(line) for line in [ zip([ column[0] for column in cursor.description ], row) for row in cursor.fetchall() ] ]
#
#     bd._cerrar_conexion()
#
#     return query_result