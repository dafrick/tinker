#!/usr/bin/env python3

import argparse
from bs4 import BeautifulSoup
import re
import requests
from typing import Tuple, List, Dict, Any, Optional

class Blurber:
    def __init__(self, url: str):
        self.url: str = url
        self.page: BeautifulSoup = self._get_page()

        self.title: Optional[str] = None
        self.website_type: Optional[str] = None
        self.authors: List[str] = []
        self.publisher: Optional[str] = None
        self.platform: Optional[str] = None

        self.title, self.authors, self.publisher = self._parse_title()
        #self.authors: List[str] = self._get_authors()
        self.website_type: str = self.get_website_type()
        #self.publisher: str = self.get_publisher()
        self.platform: str = self.get_platform()
        self.keywords: List[str] = self.get_keywords()

        # FIX: Titles like "Broken Ownership - Alex Ewerlöf Notes" need to have the publication removed from the title

    def _get_page(self) -> BeautifulSoup:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        session = requests.Session()
        response = session.get(self.url, headers=headers)
        page = BeautifulSoup(response.content, 'html.parser')
        return page

    @staticmethod
    def _extract_title_and_authors(title: str) -> Tuple[Optional[str], List[str], Optional[str]]:
        # Deal with titles of the form "AI Product Managers - by Alex Alexakis and Marily Nika" and "Construction Goes Robotic - Startup Pirate by Alex Alexakis"
        pattern = r'(.*?) - ([\s\w]*)by([\s\w]*)'
        match = re.match(pattern, title)
        title = match.group(1).strip() if match else title
        publisher = match.group(2).strip() if match and match.group(2) else None
        authors = [author.strip() for author in re.split(",|and", match.group(3))] if match and match.group(3) else []

        return title, authors, publisher

    def _parse_title(self) -> Optional[str]:
        title: Optional[str] = None
        authors: List[str] = []
        publisher: Optional[str] = None

        title_element = self.page.find('title')
        if title_element:
            title, authors, publisher = Blurber._extract_title_and_authors(title_element.text)

        # .split(" | ")[0]

        return title, authors, publisher


    def _get_authors(self) -> List[str]:
        authors_from_meta = [author['content'] for author in self.page.find_all('meta', {'name': 'author'}) if 'content' in author]
        authors_from_span = [author.text for author in self.page.find_all('span', {'class': 'author'})]
        authors_from_div = [author.text for author in self.page.find_all('div', {'class': 'author'})]
        authors = authors_from_meta + authors_from_span + authors_from_div
        return

    def get_website_type(self) -> Optional[str]:
        website_type_element = self.page.find('meta', {'name': 'citation_type'})
        return website_type_element['content'] if website_type_element else None

    def get_publisher(self) -> Optional[str]:
        publication_element = self.page.find('meta', {'name': 'citation_journal_title'})
        return publication_element['content'] if publication_element else None

    def get_platform(self) -> Optional[str]:
        platform_element = self.page.find('meta', {'name': 'citation_publisher'})
        return platform_element['content'] if platform_element else None


    def get_keywords(self) -> List[str]:
        tags = self.page.find_all('meta', {'name': 'keywords'})
        return [tag['content'] for tag in tags] if tags else []

    def __str__(self) -> str:
        title = self.get_title()
        website_type = self.get_website_type()
        authors = self.get_authors()
        publisher = self.get_publisher()
        platform = self.get_platform()
        keywords = self.get_keywords()

        blurb = f"# {title}\n\n"
        blurb += f"**Website Type:** {website_type}\n\n"
        blurb += f"**Authors:**\n"
        for author in authors:
            blurb += f"- {author}\n"
        blurb += f"\n"
        blurb += f"**Publisher:** {publisher}\n\n"
        blurb += f"**Platform:** {platform}\n\n"
        blurb += f"**Keywords:**\n"
        for keyword in keywords:
            blurb += f"- {keyword}\n"

        return blurb

import pathlib

class FileParser:
    def __init__(self, file_path: str, max_blurbs: Optional[int] = 10):
        self.file_path: pathlib.Path = pathlib.Path(file_path).resolve()
        self.blurbers = self._get_blurbers(max_blurbs)

    @staticmethod
    def _extract_url(line: str) -> Optional[str]:
        url_pattern = r'(https?://\S+)'
        match = re.search(url_pattern, line)
        return match.group(1) if match else None

    def _get_blurbers(self, max_blurbs: Optional[int]) -> List[Blurber]:
        blurbers = []
        with open(self.file_path, 'r') as f:
            for line in f:
                if max_blurbs is not None and len(blurbers) >= max_blurbs:
                    break
                blurbers.append(Blurber(FileParser._extract_url(line)))
        return blurbers

    def __str__(self) -> str:
        blurbs = []
        for blurber in self.blurbers:
            blurbs.append(str(blurber))
        return "\n\n---\n\n".join(blurbs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='URL of the web article')
    args = parser.parse_args()
    print(Blurber(args.url))


# def extract_publication(page: BeautifulSoup) -> Optional[str]:
#     publication_element = page.find('meta', {'name': 'citation_journal_title'})
#     return publication_element['content'] if publication_element else None

# def extract_publishing_platform(page: BeautifulSoup) -> Optional[str]:
#     platform_element = page.find('meta', {'name': 'citation_publisher'})
#     return platform_element['content'] if platform_element else None

# def extract_affiliations(page: BeautifulSoup) -> List[str]:
#     affiliations = page.find_all('meta', {'name': 'citation_author_institution'})
#     return [affiliation['content'] for affiliation in affiliations] if affiliations else []

# def extract_tags(page: BeautifulSoup) -> List[str]:
#     tags = page.find_all('meta', {'name': 'keywords'})
#     return [tag['content'] for tag in tags] if tags else []

# def extract_website(page: BeautifulSoup) -> Optional[str]:
#     possible_names = []
#     website_element = soup.find('meta', {'property': 'og:site_name'})
#     possible_names.append(website_element['content'] if website_element else None)

#     # Try to finde the website name from the title
#     title_element = soup.find('title')
#     if title_element is not None:
#         title_split = title_element.text.split(" | ")
#         possible_names.append(title_split[-1] if len(title_split) > 1 else None)

#     print(possible_names)

#     return next((name for name in possible_names if name is not None), None)

# def extract_article_info(url: str) -> Dict[str, Any]:
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#     }
#     session = requests.Session()
#     response = session.get(url, headers=headers)
#     soup = BeautifulSoup(response.content, 'html.parser')

#     return {
#         'title': extract_title(soup),
#         'authors': extract_authors(soup),
#         'publication': extract_publication(soup),
#         'publishing platform': extract_publishing_platform(soup),
#         'affiliation': extract_affiliations(soup),
#         'tags': extract_tags(soup),
#         'website': extract_website(soup)
#     }
