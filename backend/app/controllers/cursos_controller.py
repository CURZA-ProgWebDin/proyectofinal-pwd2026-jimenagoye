from app import db
from app.models.usuario import Usuario
from app.models.curso import Curso, Modulo, Clase


def _puede_modificar(curso, usuario_id):
    # Permite editar solo al dueño del curso o a un administrador
    usuario = Usuario.query.get(int(usuario_id))
    if not usuario:
        return False
    return usuario.rol == "administrador" or curso.creador_id == usuario.id


def _curso_activo(id):
    return Curso.query.filter_by(id=id, activo=True).first()


def listar_cursos(page, per_page, nivel, anio, categoria, busqueda):
    query = Curso.query.filter_by(activo=True)  # solo se muestran cursos activos, no eliminados

    if nivel:
        query = query.filter_by(nivel=nivel)
    if anio:
        query = query.filter_by(anio=anio)
    if categoria:
        query = query.filter_by(categoria=categoria)
    if busqueda:
        query = query.filter(Curso.titulo.ilike(f"%{busqueda}%"))

    # Ordena por fecha y pagina el resultado (grupos de "per_page" cursos)
    pagination = query.order_by(Curso.fecha_creacion.desc()).paginate(
        page=page, per_page=per_page
    )
    return {
        "cursos": [c.to_dict() for c in pagination.items],
        "total": pagination.total,
        "paginas": pagination.pages,
        "pagina_actual": page,
    }, 200


def obtener_curso(id):
    curso = _curso_activo(id)
    if not curso:
        return {"error": "Curso no encontrado"}, 404
    return curso.to_dict(include_modulos=True), 200


def crear_curso(data, creador_id):
    # Valida que los datos básicos del curso vengan en la petición
    if not data or not data.get("titulo") or not data.get("descripcion"):
        return {"error": "Título y descripción son obligatorios"}, 400

    curso = Curso(
        titulo=data["titulo"],
        descripcion=data["descripcion"],
        imagen_url=data.get("imagen_url"),
        precio=data.get("precio", 0),
        nivel=data.get("nivel"),
        anio=data.get("anio"),
        categoria=data.get("categoria"),
        creador_id=int(creador_id),
    )
    db.session.add(curso)  # agrega el objeto a la sesión de SQLAlchemy
    db.session.commit()  # guarda los cambios en la base de datos

    return {"mensaje": "Curso creado", "curso": curso.to_dict()}, 201


def actualizar_curso(id, data, usuario_id):
    curso = Curso.query.get_or_404(id)  # trae el curso o responde 404 si no existe

    if not _puede_modificar(curso, usuario_id):
        return {"error": "No podés editar este curso"}, 403

    for campo in ["titulo", "descripcion", "imagen_url", "precio", "nivel", "anio", "categoria", "activo"]:
        if data and campo in data:
            setattr(curso, campo, data[campo])

    db.session.commit()
    return {"mensaje": "Curso actualizado", "curso": curso.to_dict()}, 200


def eliminar_curso(id, usuario_id):
    curso = Curso.query.get_or_404(id)

    if not _puede_modificar(curso, usuario_id):
        return {"error": "No podés eliminar este curso"}, 403

    curso.activo = False
    db.session.commit()
    return {"mensaje": "Curso desactivado"}, 200


def crear_modulo(curso_id, data, usuario_id):
    curso = _curso_activo(curso_id)
    if not curso:
        return {"error": "Curso no encontrado"}, 404

    if not _puede_modificar(curso, usuario_id):
        return {"error": "No podés modificar este curso"}, 403

    if not data or not data.get("titulo"):
        return {"error": "El título del módulo es obligatorio"}, 400

    ultimo_orden = len(curso.modulos)
    modulo = Modulo(
        titulo=data["titulo"],
        orden=data.get("orden", ultimo_orden + 1),
        curso_id=curso_id,
    )
    db.session.add(modulo)
    db.session.commit()

    return {"mensaje": "Módulo creado", "modulo": modulo.to_dict()}, 201


def actualizar_modulo(curso_id, modulo_id, data, usuario_id):
    modulo = Modulo.query.filter_by(id=modulo_id, curso_id=curso_id).first_or_404()
    curso = modulo.curso

    if not _puede_modificar(curso, usuario_id):
        return {"error": "No podés modificar este curso"}, 403

    if "titulo" in (data or {}):
        modulo.titulo = data["titulo"]
    if "orden" in (data or {}):
        modulo.orden = data["orden"]

    db.session.commit()
    return {"mensaje": "Módulo actualizado", "modulo": modulo.to_dict()}, 200


def eliminar_modulo(curso_id, modulo_id, usuario_id):
    modulo = Modulo.query.filter_by(id=modulo_id, curso_id=curso_id).first_or_404()
    curso = modulo.curso

    if not _puede_modificar(curso, usuario_id):
        return {"error": "No podés modificar este curso"}, 403

    db.session.delete(modulo)
    db.session.commit()
    return {"mensaje": "Módulo eliminado"}, 200


def crear_clase(curso_id, modulo_id, data, usuario_id):
    modulo = Modulo.query.filter_by(id=modulo_id, curso_id=curso_id).first_or_404()

    if not _puede_modificar(modulo.curso, usuario_id):
        return {"error": "No podés modificar este curso"}, 403

    if not data or not data.get("titulo"):
        return {"error": "El título de la clase es obligatorio"}, 400

    ultimo_orden = len(modulo.clases)
    clase = Clase(
        titulo=data["titulo"],
        tipo_archivo=data.get("tipo_archivo", "video"),
        url_archivo=data.get("url_archivo"),
        duracion_minutos=data.get("duracion_minutos"),
        orden=data.get("orden", ultimo_orden + 1),
        es_gratis=data.get("es_gratis", False),
        modulo_id=modulo_id,
    )
    db.session.add(clase)
    db.session.commit()

    return {"mensaje": "Clase creada", "clase": clase.to_dict()}, 201


def actualizar_clase(curso_id, modulo_id, clase_id, data, usuario_id):
    clase = Clase.query.filter_by(id=clase_id, modulo_id=modulo_id).first_or_404()

    if clase.modulo.curso_id != curso_id:
        return {"error": "La clase no pertenece a este curso"}, 404

    if not _puede_modificar(clase.modulo.curso, usuario_id):
        return {"error": "No podés modificar este curso"}, 403

    for campo in ["titulo", "tipo_archivo", "url_archivo", "duracion_minutos", "orden", "es_gratis"]:
        if data and campo in data:
            setattr(clase, campo, data[campo])

    db.session.commit()
    return {"mensaje": "Clase actualizada", "clase": clase.to_dict()}, 200


def eliminar_clase(curso_id, modulo_id, clase_id, usuario_id):
    clase = Clase.query.filter_by(id=clase_id, modulo_id=modulo_id).first_or_404()

    if clase.modulo.curso_id != curso_id:
        return {"error": "La clase no pertenece a este curso"}, 404

    if not _puede_modificar(clase.modulo.curso, usuario_id):
        return {"error": "No podés modificar este curso"}, 403

    db.session.delete(clase)
    db.session.commit()
    return {"mensaje": "Clase eliminada"}, 200