"""API da estimativa agrícola avançada com isolamento de contas."""
from flask import Blueprint, g, jsonify, request, current_app
from sqlalchemy.exc import SQLAlchemyError
from models.database import db
from services.analise_avancada_service import AnaliseAvancadaService

analise_avancada_controller = Blueprint("analise_avancada_controller", __name__)


@analise_avancada_controller.get("/api/analise-avancada/safras/<int:safra_id>")
def consultar(safra_id):
    try:
        return jsonify(AnaliseAvancadaService().consultar(safra_id, g.usuario_id))
    except LookupError as exc:
        return jsonify({"erro": str(exc)}), 404
    except SQLAlchemyError:
        current_app.logger.exception("Falha ao consultar análise agrícola")
        return jsonify({"erro": "Não foi possível consultar a análise."}), 500


@analise_avancada_controller.put("/api/analise-avancada/safras/<int:safra_id>")
def salvar(safra_id):
    dados = request.get_json(silent=True)
    try:
        return jsonify(AnaliseAvancadaService().salvar(safra_id, g.usuario_id, dados))
    except ValueError as exc:
        return jsonify({"erro": str(exc)}), 400
    except LookupError as exc:
        return jsonify({"erro": str(exc)}), 404
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Falha ao salvar parâmetros agrícolas")
        return jsonify({"erro": "Não foi possível salvar a análise."}), 500
