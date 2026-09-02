from app import db
from app.models.usuario import Usuario
from app.models.inscripcion import Inscripcion
from app.models.curso import Curso


def _puede_gestionar(inscripcion, usuario_id):
    # Solo el propio alumno o un admin puede tocar una inscripción
    usuario = Usuario.query.get(int(usuario_id))
    if not usuario:
        return False
    return usuario.rol == "administrador" or inscripcion.estudiante_id == usuario.id


def listar_inscripciones(estudiante_id):
    # Cada alumno solo ve sus propias inscripciones (filtra por su id)
    inscripciones = Inscripcion.query.filter_by(estudiante_id=int(estudiante_id)).all()
    return [i.to_dict() for i in inscripciones], 200


def inscribirse(estudiante_id, data):
    curso_id = (data or {}).get("curso_id")
    if not curso_id:
        return {"error": "El curso es obligatorio"}, 400

    curso = Curso.query.filter_by(id=curso_id, activo=True).first()
    if not curso:
        return {"error": "Curso no encontrado"}, 404

    # Consulta SQLAlchemy: verifica si ese alumno ya está inscripto en el curso
    existente = Inscripcion.query.filter_by(
        estudiante_id=int(estudiante_id), curso_id=curso_id
    ).first()
    if existente:
        return {"error": "Ya estás inscripto en este curso"}, 409

    inscripcion = Inscripcion(
        estudiante_id=int(estudiante_id),
        curso_id=curso_id,
    )
    db.session.add(inscripcion)
    db.session.commit()

    return {"mensaje": "Inscripción exitosa", "inscripcion": inscripcion.to_dict()}, 201


def actualizar_inscripcion(id, data, usuario_id):
    inscripcion = Inscripcion.query.get_or_404(id)

    if not _puede_gestionar(inscripcion, usuario_id):
        return {"error": "No podés modificar esta inscripción"}, 403

    if "progreso" in (data or {}):
        inscripcion.progreso = data["progreso"]
    if "estado" in (data or {}):
        inscripcion.estado = data["estado"]

    db.session.commit()
    return {"mensaje": "Inscripción actualizada", "inscripcion": inscripcion.to_dict()}, 200


def cancelar_inscripcion(id, usuario_id):
    inscripcion = Inscripcion.query.get_or_404(id)

    if not _puede_gestionar(inscripcion, usuario_id):
        return {"error": "No podés cancelar esta inscripción"}, 403

    inscripcion.estado = "cancelada"
    db.session.commit()
    return {"mensaje": "Inscripción cancelada"}, 200


def mis_cursos(estudiante_id):
    inscripciones = Inscripcion.query.filter_by(
        estudiante_id=int(estudiante_id), estado="activa"
    ).all()

    cursos = []
    for insc in inscripciones:
        curso_data = insc.curso.to_dict()
        curso_data["progreso"] = insc.progreso
        cursos.append(curso_data)

    return cursos, 200