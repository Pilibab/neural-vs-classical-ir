from app.main import app


@app.route("/api/manhwa/<id>", methods=['GET'])
def get_manhwa_details(id):
    # Direct lookup in MongoDB by ID
    manhwa = ManhwaService.get_by_id(id)
    if not manhwa:
        return jsonify({"error": "Not found"}), 404
    return jsonify(manhwa), 200