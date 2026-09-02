from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.config import Config

# ORM global: convierte objetos Python en consultas SQL a la base de datos
db = SQLAlchemy()
# Gestor de JWT: crea y valida los tokens de autenticación
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Recurso no encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"error": "Error interno del servidor"}), 500

    # Cada módulo del sistema se registra como Blueprint, cada uno con su prefijo de URL
    from app.routes.auth import auth_bp
    from app.routes.usuarios import usuarios_bp
    from app.routes.cursos import cursos_bp
    from app.routes.inscripciones import inscripciones_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(usuarios_bp, url_prefix="/api/usuarios")
    app.register_blueprint(cursos_bp, url_prefix="/api/cursos")
    app.register_blueprint(inscripciones_bp, url_prefix="/api/inscripciones")

    with app.app_context():
        from app.models import usuario, curso, inscripcion
        db.create_all()  # crea las tablas si todavía no existen en la base de datos

    return app
