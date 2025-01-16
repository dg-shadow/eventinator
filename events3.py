import requests
from bs4 import BeautifulSoup

# URL of the events calendar page
url = "https://www.tottenhamhotspurstadium.com/whats-on/events-calendar/"

# Send a GET request to fetch the HTML content of the events page
response = requests.get(url)
response.raise_for_status()  # Ensure the request was successful

# Parse the main events calendar page with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all <a> elements with class 'c-feature-card__link', which contain event links
event_links = soup.find_all('a', class_='c-feature-card__link')

# Prepare a list to store event details
upcoming_events = []

# Iterate over each event link to get more details
for link in event_links:
    # Extract the event name (text inside the <a> tag)
    event_name = link.text.strip()

    # Extract the event URL (href attribute)
    event_url = link.get('href')

    # Ensure the event URL is absolute by adding the base URL if necessary
    if event_url.startswith('/'):
        event_url = f"https://www.tottenhamhotspurstadium.com{event_url}"

    # Fetch the event detail page
    event_response = requests.get(event_url)
    event_response.raise_for_status()  # Ensure the request was successful

    # Parse the event detail page with BeautifulSoup
    event_soup = BeautifulSoup(event_response.text, 'html.parser')

    # Try to extract the event time (adjust the selector based on the event detail page structure)
    event_time = "Time not available"
    event_time_element = event_soup.find(class_='event-datetime')  # You can adjust this selector based on the structure

    if event_time_element:
        event_time = event_time_element.text.strip()

    # Store the event details
    upcoming_events.append({
        'event_name': event_name,
        'event_url': event_url,
        'event_time': event_time
    })

# Output the upcoming events
if upcoming_events:
    print("Upcoming Events:")
    for event in upcoming_events:
        print(f"Event: {event['event_name']}")
        print(f"Time: {event['event_time']}")
        print(f"Link: {event['event_url']}")
        print("-" * 40)
else:
    print("No events found.")
