from SalvandoAlimentos.data.models import user as user_model
from datetime import datetime

def _existe_usuario(user_name, password):
    usuarios = user_model.obtener_usuarios_por_nombre_clave(user_name, password)
    return not len(usuarios) == 0


def _crear_sesion(id_usuario):
    hora_actual = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = hora_actual.strftime("%d/%m/%Y %H:%M:%S")
    return user_model.crear_sesion(id_usuario, dt_string)


def obtener_usuarios():
    return user_model.obtener_usuarios()


def obtener_usuario(id_usuario):
    usuario = user_model.obtener_usuario(id_usuario)
    if len(usuario) == 0:
        raise Exception("El usuario no existe")
    return usuario[0]


def create_user(name, email, user_name, password, address):
    if not _existe_usuario(name, password):
        user_model.create_user(name, email, user_name, password, address)
    else:
        raise Exception("El usuario ya existe.")


def update_user(id, name, password):
    user_model.update_user(id, name, password)


def delete_user(id_user):
    user_model.delete_user(id_user)


def user_login(user_name, password):
    if _existe_usuario(user_name, password):
        id_user = user_model.obtener_usuarios_por_nombre_clave(user_name, password)[0]
        return _crear_sesion(id_user['id'])
    else:
        raise Exception("El usuario no existe y/o la clave es incorrecta.")