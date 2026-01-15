import traceback
from datetime import datetime
from app.db.mongo import error_log_collection

err_collection = error_log_collection


class ErrorLogService:
    MAX_LOGS = 20

    @staticmethod
    def log_error(
        *,
        source: str,
        page: int,
        url: str,
        exc: Exception
    ):
        error_entry = {
            "timestamp": datetime.now(),
            "source": source,
            "page": page,
            "url": url,
            "error_type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc()
        }

        err_collection.update_one(
            {"_id": "scraper_errors"},
            {
                "$push": {
                    "logs": {
                        "$each": [error_entry],
                        "$position": 0,   # newest at top
                        "$slice": ErrorLogService.MAX_LOGS
                    }
                }
            },
            upsert=True
        )
