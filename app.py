import streamlit as st
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify
import zipfile
import io

def parse_sitemap(sitemap_url: str):
    """
    Fetch and parse the XML sitemap to extract all URLs listed within.
    Returns a list of URLs.
    """
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching sitemap: {e}")
        return []

    # Parse the XML
    soup = BeautifulSoup(response.content, "xml")
    # A typical sitemap has <url><loc>URL_HERE</loc></url> entries
    loc_tags = soup.find_all("loc")

    urls = [loc_tag.text.strip() for loc_tag in loc_tags]
    return urls

def fetch_and_convert_to_markdown(url: str) -> str:
    """
    Fetch a single URL and convert the HTML content to Markdown.
    Return the resulting Markdown string.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html_content = response.text

        # Convert HTML to Markdown
        markdown_content = markdownify(html_content)
        return markdown_content
    except requests.exceptions.RequestException as e:
        # Return an error message as markdown so that 
        # the user can see which page failed
        return f"# Error fetching {url}\n\n```\n{e}\n```"

def create_zip_file(url_to_md_map: dict) -> bytes:
    """
    Takes a dictionary of {filename: markdown_content} 
    and creates an in-memory ZIP file.
    Returns the bytes of the ZIP.
    """
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for filename, markdown_content in url_to_md_map.items():
            zip_file.writestr(filename, markdown_content)

    zip_buffer.seek(0)
    return zip_buffer.read()

def main():
    st.title("Website Crawler via Sitemap")

    sitemap_url = st.text_input("Enter the URL of your XML Sitemap", "")
    
    if st.button("Start Crawling"):
        if not sitemap_url:
            st.warning("Please provide a sitemap URL first.")
            return

        with st.spinner("Parsing sitemap..."):
            urls = parse_sitemap(sitemap_url)

        if not urls:
            st.warning("No URLs found in sitemap or an error occurred.")
            return

        st.success(f"Found {len(urls)} URL(s). Now crawling...")

        url_to_md_map = {}
        for i, url in enumerate(urls, start=1):
            st.write(f"Crawling URL {i}/{len(urls)}: {url}")
            md_content = fetch_and_convert_to_markdown(url)
            # Create a filename-safe version of the URL
            safe_filename = url.replace("https://", "").replace("http://", "")
            safe_filename = safe_filename.replace("/", "_").replace("?", "_")
            if not safe_filename.endswith(".md"):
                safe_filename += ".md"
            url_to_md_map[safe_filename] = md_content

        st.success("Crawling finished!")

        # Create ZIP in-memory
        zip_file_bytes = create_zip_file(url_to_md_map)

        # Provide a download button
        st.download_button(
            label="Download All as ZIP",
            data=zip_file_bytes,
            file_name="crawled_markdown_files.zip",
            mime="application/zip"
        )

if __name__ == "__main__":
    main()
