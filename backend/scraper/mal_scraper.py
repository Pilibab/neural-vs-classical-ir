import requests
from bs4 import BeautifulSoup
import time
import re

from app.services.error_log_service import ErrorLogService



BASE_URL = "https://myanimelist.net"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_manhwa_list(route: str = "/topmanga.php?type=manhwa&", result_lazy_limit: int = 50, test_phase: bool = False, source="MAL"):
    test_limit = 1
    test_itr = 0 


    result = []
    total_manhwa = 0
    page = 150

    while True:

        url = f"{BASE_URL}{route}limit={page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"\n⚠️ Error: Status code {response.status_code}")
            break

        # get the table that contains the manhwa 
        soup = BeautifulSoup(response.text, "html.parser")
        entries = soup.select("tr.ranking-list")

        if not entries:
            print(f"\ No more entries found. scrapped total of: {total_manhwa}")
            break

        print("=" * 30)
        print(" " * 10 + f"CURR PAGE: {page}")
        print("=" * 30)

        # 50 entries i think
        batch_idx = 1
        for entry in entries:
            try:

                if test_itr >= test_limit and test_phase:
                    return


                # Todo put this inside try?
                # ranking differs in the entry table and detail tag
                rank_tag= entry.select_one("td.rank")
                rank = rank_tag.get_text(strip=True)

                # from <h3><a>{title}<a><h3>
                # we are getting the link from a which redirects to page with manhwa details 
                detail_tag = entry.select_one("h3.manga_h3 a").get('href')

                details = scrape_detail(detail_tag)



                if details:
                    manga_id, title, synopsis_text, img_link, score, chapters, pub_date, tags, link = details
                    result.append({
                        "source": source,
                        "source_id" : manga_id,
                        "rank": rank,
                        "title": title,
                        "synopsis": synopsis_text,
                        "cover_image_url": img_link,
                        "rating": score,
                        "chapters": chapters,
                        "published_date": pub_date,
                        "tags": tags,
                        "link": link
                    })

                print(f"{batch_idx}: {title}")
                batch_idx += 1

                if test_phase:
                    test_itr += 1

                # Longer delay to be respectful to the server
                time.sleep(2)

                if len(result) >= result_lazy_limit:
                    # * tensai ka na (天才かな)?
                    yield result;

                    # does this clear it?
                    result = []

            except Exception as e: 
                ErrorLogService.log_error(
                    source=source,
                    page=page,
                    url=detail_tag,
                    exc=e,
                )

                return 
        page+=50



def scrape_detail(url: str):
    # !=============================================================
    # !FETCH + PARSE
    # !=============================================================
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    
    print(url)
    # Search for digits following "/manga/"
    
    match = re.search(r'/manga/(\d+)/', url)
    manga_id = match.group(1) if match else None


    soup = BeautifulSoup(response.text, "html.parser")
    # ! =============================================================
    # ! TITLE 
    # ! =============================================================

    # Find the first span with itemprop="name"
    # e.g. <span itemprop="name">The Greatest Estate Developer</span>
    title_tag = soup.select_one('span[itemprop="name"]')
    title = title_tag.get_text()


    # traverse the left div that contains the data to narrow search
    left_div = soup.select_one("div.leftside")

    # ! =============================================================
    # ! IMG COVER 
    # ! =============================================================

    # find image with 
    # <img class=" lazyloaded" data-src="https://cdn.myanimelist.net/images/manga/1/290131.jpg" 
    # alt="The Greatest Estate Developer" itemprop="image" 
    # src="https://cdn.myanimelist.net/images/manga/1/290131.jpg">
    img_tag = left_div.select_one('img[itemprop="image"]')
    img_link = ""

    if img_tag:
        img_link = img_tag.get('data-src') or img_tag.get('src')
    else: 
        # if doesnt exist traverse the pics then select atleast one working image 
        link_tag = left_div.find("div", style="text-align: center;").find("a")
        # TODO generate a fall back 

    # ! =============================================================
    # ! chapter, pub_date, link 
    # ! =============================================================

    chapters, pub_date, link = extract_sidebar_info(left_div)


    # ! =============================================================
    # ! TAGS
    # ! =============================================================
    tags = extract_tags(left_div)


    # <div class="rightside js-scrollfix-bottom-rel"><div style="width:728px; margin:0 auto"></div>
    right_div = soup.select_one("div.rightside")


    # ! =============================================================
    # ! SYNOPSIS
    # ! =============================================================
    synopsis_tag = right_div.select_one('span[itemprop="description"]')
    synopsis_text = extract_synopsis(synopsis_tag)

    # ! =============================================================
    # ! RATING
    # ! =============================================================
    # <div class="score-label score-9">9.03</div>
    score_tag = right_div.select_one("div.score-label")
    score = score_tag.get_text(strip=True)

    return manga_id, title, synopsis_text, img_link, score, chapters, pub_date, tags,link

def extract_synopsis(synopsis_tag):

    if not synopsis_tag or not synopsis_tag.get_text(strip=True):
        return None
    
    # Extract the text with formatting preserved
    synopsis = synopsis_tag.get_text(separator="\n", strip=True)
    
    # 1. Remove the specific MAL signature
    target_str = "[Written by MAL Rewrite]"
    synopsis = synopsis.replace(target_str, "")
    
    # 2. Clean up trailing whitespace/newlines left behind after removal
    synopsis = synopsis.strip()
    
    return synopsis if synopsis else None

# Assuming 'left_div' is the <div class="leftside"> from your HTML
def extract_sidebar_info(left_div):
    # 1. Chapters
    chapters_label = left_div.find("span", string="Chapters:")

    if chapters_label:
        # .next_sibling gets the text right after the </span>
        chapters = chapters_label.next_sibling.strip()

    # 2. Published Date
    published_label = left_div.find("span", string="Published:")
    if published_label:
        pub_date = published_label.next_sibling.strip()

    # 3. External Link (Official Site)
    # This is in the 'external_links' div
    link_tag = left_div.select_one(".external_links a.link")
    link = link_tag['href'] if link_tag else "No link found"

    return chapters, pub_date, link


def extract_tags(left_div):
    """
    Extract only the Genres (not Themes) from the page.
    Returns a comma-separated string of genres.
    """
    # Find the div that contains "Genres:" text
    genre_div = left_div.find("span", string="Genres:")
    
    if not genre_div:
        return ""
    
    # Get the parent div (the spaceit_pad div)
    genre_container = genre_div.parent
    
    # Find all spans with itemprop="genre" within this specific container
    genre_spans = genre_container.find_all("span", itemprop="genre")
    
    # Extract text and use set to avoid duplicates
    unique_genres = {span.get_text().strip() for span in genre_spans}
    
    return ", ".join(sorted(unique_genres))


def extract_themes(left_div):
    """
    Extract only the Themes (not Genres) from the page.
    Returns a comma-separated string of themes.
    """
    # Find the div that contains "Themes:" text
    theme_div = left_div.find("span", string="Themes:")
    
    if not theme_div:
        return ""
    
    # Get the parent div (the spaceit_pad div)
    theme_container = theme_div.parent
    
    # Find all spans with itemprop="genre" within this specific container
    theme_spans = theme_container.find_all("span", itemprop="genre")
    
    # Extract text and use set to avoid duplicates
    unique_themes = {span.get_text().strip() for span in theme_spans}
    
    return ", ".join(sorted(unique_themes))



