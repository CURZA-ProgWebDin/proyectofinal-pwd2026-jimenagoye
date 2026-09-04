from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.usuario import Usuario


def rol_requerido(*roles_permitidos):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()  # valida que el token llegue firmado y no haya expirado
            usuario_id = get_jwt_identity()  # lee el id del usuario guardado dentro del token
            usuario = Usuario.query.get(int(usuario_id))  # busca ese usuario en la base de datos
            if not usuario or not usuario.activo or usuario.rol not in roles_permitidos:
                # El usuario no existe, está desactivado o su rol no es el correcto
                return jsonify({"error": "No tenés permiso para esta acción"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator