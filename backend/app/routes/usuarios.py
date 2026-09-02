from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.usuarios_controller import (
    actualizar_usuario,
    eliminar_usuario,
    listar_usuarios,
    mi_perfil,
    obtener_usuario,
)
from app.decorators.roles import rol_requerido

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/", methods=["GET"])
@jwt_required()
def index():
    data, status = listar_usuarios(
        page=request.args.get("page", 1, type=int),
        per_page=request.args.get("per_page", 20, type=int),
    )
    return jsonify(data), status


@usuarios_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def show(id):
    data, status = obtener_usuario(id)
    return jsonify(data), status


@usuarios_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update(id):
    data, status = actualizar_usuario(id, get_jwt_identity(), request.get_json())
    return jsonify(data), status


@usuarios_bp.route("/<int:id>", methods=["DELETE"])
@rol_requerido("administrador")  # desactivar usuarios es exclusivo del rol admin
def destroy(id):
    data, status = eliminar_usuario(id, get_jwt_identity())
    return jsonify(data), status


@usuarios_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    data, status = mi_perfil(get_jwt_identity())
    return jsonify(data), status
