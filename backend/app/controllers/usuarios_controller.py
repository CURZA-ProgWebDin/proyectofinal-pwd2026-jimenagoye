from app import db
from app.models.usuario import Usuario


def listar_usuarios(page, per_page):
    pagination = Usuario.query.paginate(page=page, per_page=per_page)
    return {
        "usuarios": [u.to_dict() for u in pagination.items],
        "total": pagination.total,
        "paginas": pagination.pages,
        "pagina_actual": page,
    }, 200


def obtener_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return usuario.to_dict(), 200


def actualizar_usuario(id, usuario_id, data):
    if int(usuario_id) != id:
        return {"error": "No podés editar otro usuario"}, 403

    usuario = Usuario.query.get_or_404(id)

    if "nombre" in data:
        usuario.nombre = data["nombre"]
    if "biografia" in data:
        usuario.biografia = data["biografia"]
    if "avatar_url" in data:
        usuario.avatar_url = data["avatar_url"]

    db.session.commit()
    return {"mensaje": "Usuario actualizado", "usuario": usuario.to_dict()}, 200


def eliminar_usuario(id, admin_id):
    if int(admin_id) == id:
        return {"error": "No podés desactivar tu propia cuenta"}, 400

    usuario = Usuario.query.get_or_404(id)
    usuario.activo = False
    db.session.commit()
    return {"mensaje": "Usuario desactivado"}, 200


def mi_perfil(usuario_id):
    usuario = Usuario.query.get_or_404(int(usuario_id))
    return usuario.to_dict(), 200
