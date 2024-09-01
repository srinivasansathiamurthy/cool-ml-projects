import os
import requests
from bs4 import BeautifulSoup
import re

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

def extract_transcript_content(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    sub_head = soup.select_one('p.cnnTransSubHead').get_text(strip=True)
    body_texts = [p.get_text(strip=True) for p in soup.select('p.cnnBodyText')]
    return sub_head, "\n".join(body_texts)

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

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
            sub_head, body_text = extract_transcript_content(transcript_content)
            filename = sanitize_filename(f"{sub_head.replace(' ', '_')}.txt")
            save_transcript(body_text, filename)
        
        next_page = BeautifulSoup(page_content, 'html.parser').select_one('a[href*="?start_fileid="]')
        if next_page:
            url = f"https://transcripts.cnn.com{next_page['href']}"
        else:
            break

if __name__ == "__main__":
    scrape_transcripts()
