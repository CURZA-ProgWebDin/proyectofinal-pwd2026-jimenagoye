from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.auth_controller import (
    iniciar_sesion,
    refrescar_token,
    registrar_usuario,
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():  # crea una cuenta nueva
    data, status = registrar_usuario(request.get_json())
    return jsonify(data), status


@auth_bp.route("/login", methods=["POST"])
def login():  # autentica al usuario y entrega los tokens
    data, status = iniciar_sesion(request.get_json())
    return jsonify(data), status


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)  # esta ruta solo acepta el refresh token, no el access token
def refresh():
    data, status = refrescar_token(get_jwt_identity())
    return jsonify(data), status