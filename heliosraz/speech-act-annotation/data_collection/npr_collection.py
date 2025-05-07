from bs4 import BeautifulSoup
import requests

url = "https://www.npr.org/programs/all-things-considered/archive"
page = requests.get(url)
count = 0
soup = BeautifulSoup(page.text, "html.parser")
for month in soup.find_all("ul", class_="months"):
    month_links = month.find_all("a")
    for l in month_links:
        month_link = l.get("href")
        month_page = requests.get("https://www.npr.org/" + month_link)
        month_soup = BeautifulSoup(month_page.text, "html.parser")
        for h3 in month_soup.find_all("h3", class_="program-segment__title"):
            article_link = h3.find("a", href=True).get("href")
            story_page = requests.get(article_link)
            story_soup = BeautifulSoup(story_page.text, "html.parser")
            if story_soup.find(class_="transcript storytext"):
                with open(
                    "../data/npr/" + article_link.split("/")[-2] + ".txt",
                    "w",
                    encoding="utf-8",
                ) as f:
                    print(article_link.split("/")[-2] + ".txt")
                    content = story_soup.find(class_="transcript storytext").get_text()
                    f.write(content)
                    count += 1
                    print("percent complete:", count / 2695 * 100, "%")
