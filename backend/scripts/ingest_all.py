# calls the scrapper -> ... -> put the manhwa_data to db
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.pipelines.ingest_pipeline import ingest
from scraper.mal_scraper import get_manhwa_list
from app.pipelines.embed_pipeline import embed_pipeline

def run_ingest():
    # get_manhwa_list -> [{},{},..{}] where {} are manhwa data so each {} are individual manhwa

    for raw_batch in get_manhwa_list(test_phase=True):

        for raw_manhwa in raw_batch: 
            processed_data = ingest(raw_manhwa)

            # if processed_data:  # only embed if ingest succeeded
                # embed_pipeline(processed_data)
        
if __name__ == "__main__": 
    run_ingest()