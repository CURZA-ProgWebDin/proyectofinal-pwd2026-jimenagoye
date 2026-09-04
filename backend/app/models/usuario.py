from app import db
from datetime import datetime, timezone


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default="alumno")
    avatar_url = db.Column(db.String(500))
    biografia = db.Column(db.Text)
    fecha_registro = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    activo = db.Column(db.Boolean, default=True)

    # Relaciones SQLAlchemy: un usuario crea muchos cursos y tiene muchas inscripciones
    cursos_creados = db.relationship(
        "Curso", backref="creador", lazy=True,
        foreign_keys="Curso.creador_id"
    )
    inscripciones = db.relationship(
        "Inscripcion", backref="estudiante", lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "rol": self.rol,
            "avatar_url": self.avatar_url,
            "biografia": self.biografia,
            "fecha_registro": self.fecha_registro.isoformat(),
            "activo": self.activo,
        }
