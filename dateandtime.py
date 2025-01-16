import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse

def fetch_html(url):
    """Fetches HTML content from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def extract_datetime_from_html(html):
    """Extracts datetime objects from HTML content."""
    soup = BeautifulSoup(html, 'html.parser')
    fixture_elements = soup.find_all('div', class_='FixtureHero__kickoff')
    extracted_datetimes = []

    for fixture in fixture_elements:
        datetime_element = fixture.find('p')  # Date and time (e.g., "15 January 20:00")

        if datetime_element:
            datetime_string = datetime_element.text.strip()
            try:
                # Attempt to parse the string as a datetime
                datetime_parsed = parse(datetime_string, fuzzy=True)
                extracted_datetimes.append(datetime_parsed)
            except ValueError:
                # Ignore strings that cannot be parsed as dates
                continue

    return extracted_datetimes

# URL to scrape
url = "https://www.tottenhamhotspur.com/fixtures/men/"

# Fetch the HTML content
html_content = fetch_html(url)

if html_content:
    # Extract datetime objects
    datetimes = extract_datetime_from_html(html_content)
    if datetimes:
        print("Extracted dates and times:")
        for dt in datetimes:
            print(dt)
    else:
        print("No valid dates and times found.")
