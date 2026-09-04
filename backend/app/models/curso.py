from app import db
from datetime import datetime, timezone


class Curso(db.Model):
    __tablename__ = "cursos"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen_url = db.Column(db.String(500))
    precio = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    nivel = db.Column(db.String(50))
    anio = db.Column(db.Integer)
    categoria = db.Column(db.String(100))
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    creador_id = db.Column(
        db.Integer, db.ForeignKey("usuarios.id"), nullable=False
    )
    # Un curso tiene muchos módulos (ordenados) y muchas inscripciones;
    # "delete-orphan" borra los hijos si se borra el curso
    modulos = db.relationship(
        "Modulo", backref="curso", lazy=True,
        order_by="Modulo.orden", cascade="all, delete-orphan"
    )
    inscripciones = db.relationship(
        "Inscripcion", backref="curso", lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self, include_modulos=False):
        data = {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "imagen_url": self.imagen_url,
            "precio": float(self.precio),
            "nivel": self.nivel,
            "anio": self.anio,
            "categoria": self.categoria,
            "activo": self.activo,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "creador_id": self.creador_id,
            "creador_nombre": self.creador.nombre if self.creador else None,
            "total_inscripciones": len(self.inscripciones),
        }
        if include_modulos:
            data["modulos"] = [m.to_dict() for m in self.modulos]
        return data


class Modulo(db.Model):
    __tablename__ = "modulos"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    orden = db.Column(db.Integer, nullable=False, default=0)
    curso_id = db.Column(
        db.Integer, db.ForeignKey("cursos.id"), nullable=False
    )
    clases = db.relationship(
        "Clase", backref="modulo", lazy=True,
        order_by="Clase.orden", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "orden": self.orden,
            "clases": [c.to_dict() for c in self.clases],
        }


class Clase(db.Model):
    __tablename__ = "clases"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    tipo_archivo = db.Column(db.String(20), nullable=False, default="video")
    url_archivo = db.Column(db.String(500))
    duracion_minutos = db.Column(db.Integer)
    orden = db.Column(db.Integer, nullable=False, default=0)
    es_gratis = db.Column(db.Boolean, default=False)
    modulo_id = db.Column(
        db.Integer, db.ForeignKey("modulos.id"), nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "tipo_archivo": self.tipo_archivo,
            "url_archivo": self.url_archivo,
            "duracion_minutos": self.duracion_minutos,
            "orden": self.orden,
            "es_gratis": self.es_gratis,
            "modulo_id": self.modulo_id,
        }
