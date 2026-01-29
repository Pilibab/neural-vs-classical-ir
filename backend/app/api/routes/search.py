# search.py: The endpoint where the user sends a synopsis.
from flask import Blueprint,request, jsonify
from pydantic import ValidationError

from models.search import searchReqSchema
from services.search_service import search_manhwa
from services.manhwa_service import ManhwaService
from utils.format_search_result import format_search_results
from utils.text_cleaner import clean_text
from utils.embed_query import get_query_embedding

# Create the Blueprint
search_bp = Blueprint('search_bp', __name__)

@search_bp.route("/api/search", methods=['POST'])
def search():
    data = request.get_json()


    print("\n\n--- DEBUG: Incoming Request Data ---")
    print(f"Payload: {data}")
    print(f"Type: {type(data)}")


    # check if request is valid 
    try:
        valid_data = searchReqSchema(**data)
        print("\n\n--- DEBUG: Validation Successful ---")
        print(f"Validated Object: {valid_data}")

    except ValidationError as e:
        print("error:",e)
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400
    
    print(f"--- DEBUG: Calling search with: {valid_data.synopsis} ---")

    cleaned_text = clean_text(valid_data.synopsis)

    embedded_synopsis = get_query_embedding(cleaned_text)

    # proceed with search service + clean up 
    search_result = format_search_results(search_manhwa(embedded_synopsis))


    service = ManhwaService()


    return jsonify({
        "status": "success",
        "count": len(search_result),
        "ranking":search_result,
    }), 200