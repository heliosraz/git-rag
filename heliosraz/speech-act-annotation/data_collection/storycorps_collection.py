import requests
from bs4 import BeautifulSoup


def get_story_links(list_url):
    response = requests.get(list_url, headers=headers)
    print(list_url)
    print(f"Request to {list_url} returned status code {response.status_code}")
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")
    print(f"Found {len(links)} links")
    urls = [
        link["href"] for link in links if link["href"].startswith("http")
    ]  # Ensure it's a full URL
    print(urls)
    return urls


def get_transcript(story_url):
    response = requests.get(story_url, headers=headers)
    print(f"Request to {story_url} returned status code {response.status_code}")
    soup = BeautifulSoup(response.text, "html.parser")
    transcript = soup.find("div", class_="transcript-container")
    print(f"Transcript found: {bool(transcript)}")
    return transcript.text.strip() if transcript else "No transcript found"


# Main scraper function
def scrape_storycorps(base_url):
    story_links = get_story_links(base_url)
    if not story_links:  # Debug check
        print("No story links were found. Check the get_story_links function.")
    transcripts = {}
    for url in story_links:
        transcripts[url] = get_transcript(url)
    return transcripts


if __name__ == "__main__":
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    base_list_url = "https://storycorps.org/stories/"
    transcripts = scrape_storycorps(base_list_url)
    if not transcripts:  # Debug check
        print("No transcripts were scraped. Check the scrape_storycorps function.")
    index = 1
    for url, transcript in transcripts.items():
        print(f"Transcript for {url}:")
        print(transcript)
        print("written to file:", "../data/storycorps/" + str(index) + ".txt")
        print("\n---\n")
        if not transcript == "No transcript found":
            with open(
                "../data/storycorps/" + str(index) + ".txt", "w", encoding="utf-8"
            ) as f:
                f.write(transcript)
            index += 1
