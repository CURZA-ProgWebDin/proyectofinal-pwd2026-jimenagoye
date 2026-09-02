import bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
from app import db
from app.models.usuario import Usuario

ROLES_VALIDOS_REGISTRO = ("alumno", "creador")


def _generar_tokens(usuario):
    claims = {"rol": usuario.rol, "nombre": usuario.nombre}
    # El access token se usa en cada petición; el refresh sirve para renovarlo cuando expira
    access = create_access_token(identity=str(usuario.id), additional_claims=claims)
    refresh = create_refresh_token(identity=str(usuario.id), additional_claims=claims)
    return {"token": access, "refresh_token": refresh}


def registrar_usuario(data):
    if not data or not data.get("email") or not data.get("password"):
        return {"error": "Email y contraseña son obligatorios"}, 400

    rol = data.get("rol", "alumno")
    if rol not in ROLES_VALIDOS_REGISTRO:
        return {"error": "Rol no válido"}, 400

    if Usuario.query.filter_by(email=data["email"]).first():
        # Consulta SQLAlchemy: si ya existe un usuario con ese email, no se repite
        return {"error": "El email ya está registrado"}, 409

    # bcrypt guarda la contraseña como un hash, nunca en texto plano
    password_hash = bcrypt.hashpw(
        data["password"].encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    usuario = Usuario(
        nombre=data.get("nombre", ""),
        email=data["email"],
        password_hash=password_hash,
        rol=rol,
        biografia=data.get("biografia", ""),
    )
    db.session.add(usuario)
    db.session.commit()

    tokens = _generar_tokens(usuario)
    return {"mensaje": "Usuario registrado", "usuario": usuario.to_dict(), **tokens}, 201


def iniciar_sesion(data):
    if not data or not data.get("email") or not data.get("password"):
        return {"error": "Email y contraseña son obligatorios"}, 400

    # Consulta SQLAlchemy: trae el usuario que tenga ese email
    usuario = Usuario.query.filter_by(email=data["email"]).first()
    if not usuario or not bcrypt.checkpw(
        data["password"].encode("utf-8"),
        usuario.password_hash.encode("utf-8"),
    ):
        # checkpw compara la contraseña enviada contra el hash guardado
        return {"error": "Credenciales inválidas"}, 401

    if not usuario.activo:
        return {"error": "El usuario está desactivado"}, 403

    tokens = _generar_tokens(usuario)
    return {"usuario": usuario.to_dict(), **tokens}, 200


def refrescar_token(usuario_id):
    # Solo renueva si el usuario sigue existiendo y está activo
    usuario = Usuario.query.filter_by(id=int(usuario_id), activo=True).first()
    if not usuario:
        return {"error": "Usuario inválido"}, 401

    claims = {"rol": usuario.rol, "nombre": usuario.nombre}
    # Devuelve un access token nuevo para que el frontend siga autenticado
    token = create_access_token(
        identity=str(usuario.id), additional_claims=claims
    )
    return {"token": token}, 200