from flask import Blueprint, request, jsonify
from datetime import datetime
from models import ExcursionManager

excursions_bp = Blueprint("excursions_bp", __name__)
excursions = ExcursionManager()

@excursions_bp.route("/excursions", methods=["GET"])
def get_excursions():
    data = excursions.get_all()
    return jsonify([{
        "id": e.id,
        "date": e.date.isoformat(),
        "guide": e.guide,
        "n_visitors": e.n_visitors,
        "phone": e.phone
    } for e in data])

@excursions_bp.route("/excursions/<int:excursion_id>", methods=["GET"])
def get_excursion(excursion_id):
    e = excursions.get(excursion_id)
    if not e:
        return jsonify({"error": "Excursion not found"}), 404
    return jsonify({
        "id": e.id,
        "date": e.date.isoformat(),
        "guide": e.guide,
        "n_visitors": e.n_visitors,
        "phone": e.phone
    })

@excursions_bp.route("/excursions", methods=["POST"])
def create_excursion():
    data = request.get_json()
    excursions.post(datetime.fromisoformat(data["date"]), data["n_visitors"], data["phone"])
    return jsonify({"message": "excursion created"}), 201