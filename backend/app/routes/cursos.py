from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.cursos_controller import (
    actualizar_clase,
    actualizar_curso,
    actualizar_modulo,
    crear_clase,
    crear_curso,
    crear_modulo,
    eliminar_clase,
    eliminar_curso,
    eliminar_modulo,
    listar_cursos,
    obtener_curso,
)
from app.decorators.roles import rol_requerido

cursos_bp = Blueprint("cursos", __name__)


@cursos_bp.route("/", methods=["GET"])
def index():  # ruta pública: cualquiera puede ver el catálogo sin estar logueado
    data, status = listar_cursos(
        page=request.args.get("page", 1, type=int),
        per_page=request.args.get("per_page", 12, type=int),
        nivel=request.args.get("nivel"),
        anio=request.args.get("anio", type=int),
        categoria=request.args.get("categoria"),
        busqueda=request.args.get("q"),
    )
    return jsonify(data), status


@cursos_bp.route("/<int:id>", methods=["GET"])
def show(id):
    data, status = obtener_curso(id)
    return jsonify(data), status


@cursos_bp.route("/", methods=["POST"])
@jwt_required()  # exige un token JWT válido
@rol_requerido("creador", "administrador")  # y que el rol sea creador o admin
def store():
    data, status = crear_curso(request.get_json(), get_jwt_identity())
    return jsonify(data), status


@cursos_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
@rol_requerido("creador", "administrador")
def update(id):
    data, status = actualizar_curso(id, request.get_json(), get_jwt_identity())
    return jsonify(data), status


@cursos_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@rol_requerido("creador", "administrador")
def destroy(id):
    data, status = eliminar_curso(id, get_jwt_identity())
    return jsonify(data), status


@cursos_bp.route("/<int:curso_id>/modulos", methods=["POST"])
@jwt_required()
@rol_requerido("creador", "administrador")
def add_modulo(curso_id):
    data, status = crear_modulo(curso_id, request.get_json(), get_jwt_identity())
    return jsonify(data), status


@cursos_bp.route("/<int:curso_id>/modulos/<int:modulo_id>", methods=["PUT"])
@jwt_required()
@rol_requerido("creador", "administrador")
def update_modulo(curso_id, modulo_id):
    data, status = actualizar_modulo(
        curso_id, modulo_id, request.get_json(), get_jwt_identity()
    )
    return jsonify(data), status


@cursos_bp.route("/<int:curso_id>/modulos/<int:modulo_id>", methods=["DELETE"])
@jwt_required()
@rol_requerido("creador", "administrador")
def destroy_modulo(curso_id, modulo_id):
    data, status = eliminar_modulo(curso_id, modulo_id, get_jwt_identity())
    return jsonify(data), status


@cursos_bp.route(
    "/<int:curso_id>/modulos/<int:modulo_id>/clases", methods=["POST"]
)
@jwt_required()
@rol_requerido("creador", "administrador")
def add_clase(curso_id, modulo_id):
    data, status = crear_clase(curso_id, modulo_id, request.get_json(), get_jwt_identity())
    return jsonify(data), status


@cursos_bp.route(
    "/<int:curso_id>/modulos/<int:modulo_id>/clases/<int:clase_id>",
    methods=["PUT"],
)
@jwt_required()
@rol_requerido("creador", "administrador")
def update_clase(curso_id, modulo_id, clase_id):
    data, status = actualizar_clase(
        curso_id, modulo_id, clase_id, request.get_json(), get_jwt_identity()
    )
    return jsonify(data), status


@cursos_bp.route(
    "/<int:curso_id>/modulos/<int:modulo_id>/clases/<int:clase_id>",
    methods=["DELETE"],
)
@jwt_required()
@rol_requerido("creador", "administrador")
def destroy_clase(curso_id, modulo_id, clase_id):
    data, status = eliminar_clase(curso_id, modulo_id, clase_id, get_jwt_identity())
    return jsonify(data), status