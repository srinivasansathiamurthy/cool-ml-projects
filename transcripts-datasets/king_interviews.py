import os
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://transcripts.cnn.com/show/lkl"
OUTPUT_DIR = "./transcripts"
MAX_PAGES = 15

def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_transcripts(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    transcripts = []
    for link in soup.select('a[href*="/show/lkl/date/"]'):
        transcripts.append(link['href'])
    return transcripts

def save_transcript(content, filename):
    with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as file:
        file.write(content)

def scrape_transcripts():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    url = BASE_URL
    for page_num in range(MAX_PAGES):
        page_content = fetch_page(url)
        transcript_links = parse_transcripts(page_content)
        
        for link in transcript_links:
            transcript_url = f"https://transcripts.cnn.com{link}"
            transcript_content = fetch_page(transcript_url)
            save_transcript(transcript_content, f"interview_{page_num}_{transcript_links.index(link)}.txt")
        
        next_page = BeautifulSoup(page_content, 'html.parser').select_one('a[href*="?start_fileid="]')
        if next_page:
            url = f"https://transcripts.cnn.com{next_page['href']}"
        else:
            break

if __name__ == "__main__":
    scrape_transcripts()
