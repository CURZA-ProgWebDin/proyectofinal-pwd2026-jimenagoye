from app import db
from datetime import datetime, timezone


class Inscripcion(db.Model):
    __tablename__ = "inscripciones"

    id = db.Column(db.Integer, primary_key=True)
    fecha_inscripcion = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    estado = db.Column(db.String(20), nullable=False, default="activa")
    progreso = db.Column(db.Float, nullable=False, default=0.0)

    estudiante_id = db.Column(
        db.Integer, db.ForeignKey("usuarios.id"), nullable=False
    )
    curso_id = db.Column(
        db.Integer, db.ForeignKey("cursos.id"), nullable=False
    )

    # Restricción a nivel de base de datos: un estudiante no puede repetir el mismo curso
    __table_args__ = (
        db.UniqueConstraint("estudiante_id", "curso_id", name="uq_estudiante_curso"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "fecha_inscripcion": self.fecha_inscripcion.isoformat(),
            "estado": self.estado,
            "progreso": self.progreso,
            "estudiante_id": self.estudiante_id,
            "curso_id": self.curso_id,
            "curso_titulo": self.curso.titulo if self.curso else None,
            "estudiante_nombre": self.estudiante.nombre if self.estudiante else None,
        }
