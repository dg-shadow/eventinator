from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL to scrape
url = "https://www.tottenhamhotspurstadium.com/whats-on/events-calendar/"
driver.get(url)

# Wait for the events section to be fully loaded (target the anchor elements with the 'c-feature-card__link' class)
try:
    # Explicit wait until the anchor elements are loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'c-feature-card__link'))
    )

    # Find all anchor elements containing the event details
    event_links = driver.find_elements(By.CLASS_NAME, 'c-feature-card__link')

    # Prepare a list to store event details
    upcoming_events = []

    for link in event_links:
        # Extract the event name (text inside the <a> tag)
        event_name = link.text.strip()
        # Extract the event URL
        event_url = link.get_attribute('href')

        # Visit the event URL to get more details (e.g., time)
        driver.get(event_url)

        # Wait for the event page to load (you can customize the element based on the event page structure)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'event-datetime'))
        )

        # Extract the event time (adjust the selector based on the actual structure of the event page)
        try:
            event_time = driver.find_element(By.CLASS_NAME, 'event-datetime').text.strip()
        except:
            event_time = "Time not available"

        # Store the event details
        upcoming_events.append({
            'event_name': event_name,
            'event_url': event_url,
            'event_time': event_time
        })

        # Go back to the events calendar page
        driver.back()

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

finally:
    # Close the browser
    driver.quit()
