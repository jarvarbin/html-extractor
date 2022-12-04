from bs4 import BeautifulSoup, Comment
import requests
import json

def extract_links_and_files(url):
    # Use requests to fetch the HTML from the specified URL.
    response = requests.get(url)
    html = response.text

    # Use BeautifulSoup to parse the HTML.
    soup = BeautifulSoup(html, "html.parser")

    # Extract all the links and files from the HTML.
    links = []
    files = []
    comments = []
    scripts = []
    urls = []
    for a in soup.find_all("a"):
        href = a.get("href")
        if href:
            links.append(href)
            if href.startswith("http"):
                urls.append(href)

    for img in soup.find_all("img"):
        src = img.get("src")
        if src:
            files.append(src)

    for script in soup.find_all("script"):
        src = script.get("src")
        if src:
            files.append(src)
        else:
            scripts.append(script.text)

    for link in soup.find_all("link"):
        href = link.get("href")
        if href:
            files.append(href)

    for comment in soup(text=lambda text: isinstance(text, Comment)):
        comments.append(comment.extract())

    return links, files, comments, scripts, urls


def main():
    url = "https://www.example.com/"
    links, files, comments, scripts, urls = extract_links_and_files(url)

    # Save the links, files, comments, scripts, and URLs to a JSON file.
    data = {
        "links": links,
        "files": files,
        "comments": comments,
        "scripts": scripts,
        "urls": urls,
    }
    with open("links_and_files.json", "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()
