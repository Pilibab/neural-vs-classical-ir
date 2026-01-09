# orchestration + validation of batch[idx]
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from utils.normalize_manhwa_data import normalize_manhwa_data

def ingest(manhwa_data):
    title, synopsis_text, img_link, score, chapters, pub_date, tags,link = manhwa_data
    title, synopsis_text, img_link, score, chapters, pub_date, tags,link = normalize_manhwa_data (rank)

