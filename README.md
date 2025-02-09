# Streamlit Sitemap Crawler

A simple Streamlit application that crawls all URLs from an XML sitemap, converts
each page to Markdown, and lets you download everything as a ZIP of Markdown files.

## Features

- **XML Sitemap Parser**: Provide a sitemap URL and automatically extract all URLs.
- **HTML to Markdown**: Fetch each page and convert HTML to Markdown.
- **Bulk Download**: Download all pages in a single ZIP file.

## Requirements

- Python 3.7+
- [Streamlit](https://streamlit.io/)
- [Requests](https://docs.python-requests.org/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [markdownify](https://pypi.org/project/markdownify/)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
