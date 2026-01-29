from flask import Blueprint, jsonify
from services.manhwa_service import ManhwaService

# Create the Blueprint
manhwa_bp = Blueprint('manhwa_bp', __name__)


@manhwa_bp.route("/api/manhwa/<source>/<source_id>", methods=['GET'])
def get_manhwa_details(source: str, source_id: str):
    try:
        manhwa = ManhwaService()
        # Ensure source_id is handled correctly (MAL is int, others might be str)
        search_id = int(source_id) if source_id.isdigit() else source_id
        
        data = manhwa.get_by_source(source, search_id)

        if not data:
            return jsonify({"error": "Not found"}), 404

        # CRITICAL: Convert MongoDB ObjectId to string before returning
        if "_id" in data:
            data["_id"] = str(data["_id"])

        return jsonify(data), 200

    except Exception as e:
        print(f"ERROR: {str(e)}") # This will show in your terminal
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500