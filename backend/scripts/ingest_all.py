# calls the scrapper -> ... -> put the manhwa_data to db



from scraper.mal_scraper import get_manhwa_list

def run_ingest():
    # get_manhwa_list -> [{},{},..{}] where {} are manhwa data so each {} are individual manhwa
    for batch in get_manhwa_list(): 
        # call ingest_pipeline here
        pass

if __name__ == "__main__": 
    pass