from flask import Blueprint, request, jsonify
from datetime import datetime
from models import PollManager

polls_bp = Blueprint("polls_bp", __name__)
polls = PollManager()

@polls_bp.route("/polls", methods=["POST"])
def create_poll():
    data = request.get_json()
    week_start = datetime.fromisoformat(data["week_start"]).date()
    week_end = datetime.fromisoformat(data["week_end"]).date()
    polls.post(week_start, week_end)
    return jsonify({"message": "poll created"}), 201

@polls_bp.route("/polls/<int:poll_id>", methods=["GET"])
def get_poll(poll_id):
    poll = polls.get(poll_id)
    if not poll:
        return jsonify({"error": "Poll not found"}), 404

    return jsonify({
        "id": poll.id,
        "week_start": poll.week_start.isoformat(),
        "week_end": poll.week_end.isoformat(),
        "is_active": poll.is_active,
        "excursions": [
            {
                "id": e.id,
                "datetime": e.datetime.isoformat() if hasattr(e, 'datetime') else e.date.isoformat(),
                "n_visitors": e.n_visitors,
                "guide": e.guide,
                "phone": e.phone
            }
            for e in poll.excursions
        ]
    })

@polls_bp.route("/polls", methods=["GET"])
def get_all_polls():
    all_polls = polls.get_all()
    return jsonify([
        {
            "id": p.id,
            "week_start": p.week_start.isoformat(),
            "week_end": p.week_end.isoformat(),
            "is_active": p.is_active,
            "excursions_count": len(p.excursions)
        }
        for p in all_polls
    ])