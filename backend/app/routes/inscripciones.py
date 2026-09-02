from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.inscripciones_controller import (
    actualizar_inscripcion,
    cancelar_inscripcion,
    inscribirse,
    listar_inscripciones,
    mis_cursos,
)
from app.decorators.roles import rol_requerido

inscripciones_bp = Blueprint("inscripciones", __name__)


@inscripciones_bp.route("/", methods=["GET"])
@jwt_required()
def index():
    data, status = listar_inscripciones(get_jwt_identity())
    return jsonify(data), status


@inscripciones_bp.route("/", methods=["POST"])
@jwt_required()  # hay que estar logueado para inscribirse
@rol_requerido("alumno")  # y ser alumno; un creador no se inscribe a cursos
def store():
    data, status = inscribirse(get_jwt_identity(), request.get_json())
    return jsonify(data), status


@inscripciones_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
@rol_requerido("alumno", "administrador")
def update(id):
    data, status = actualizar_inscripcion(id, request.get_json(), get_jwt_identity())
    return jsonify(data), status


@inscripciones_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@rol_requerido("alumno")
def destroy(id):
    data, status = cancelar_inscripcion(id, get_jwt_identity())
    return jsonify(data), status


@inscripciones_bp.route("/mis-cursos", methods=["GET"])
@jwt_required()
def cursos_inscriptos():
    data, status = mis_cursos(get_jwt_identity())
    return jsonify(data), status