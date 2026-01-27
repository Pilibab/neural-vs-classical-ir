from flask import Blueprint, jsonify
from services.manhwa_service import ManhwaService

# Create the Blueprint
manhwa_bp = Blueprint('manhwa_bp', __name__)


@manhwa_bp.route("/api/manhwa/<source>/<source_id>", methods=['GET'])
def get_manhwa_details(source: str,source_id: str):
    # Direct lookup in MongoDB by ID
    manhwa = ManhwaService.get_by_source(source, source_id)

    if not manhwa:
        return jsonify({"error": "Not found"}), 404
    return jsonify(manhwa), 200