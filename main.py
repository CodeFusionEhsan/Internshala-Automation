import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Constants
INTERNSHALA_URL = "https://internshala.com"
EMAIL = "your_email@gmail.com"  # Replace with your email
PASSWORD = "your_password"  # Replace with your email password
RECIPIENT_EMAIL = "recipient_email@example.com"  # Replace with recipient email
WEBDRIVER_PATH = "/path/to/chromedriver"  # Replace with your WebDriver path

# Initialize WebDriver
def init_driver():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service(WEBDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Scrape Internships and Jobs
def scrape_internships(driver, domain):
    driver.get(INTERNSHALA_URL)
    time.sleep(5)  # Wait for the page to load

    # Search for internships in the specified domain
    search_box = driver.find_element(By.NAME, "keywords")
    search_box.send_keys(domain)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)  # Wait for the search results to load

    # Parse the page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    internships = []

    # Find all internship listings
    for item in soup.find_all("div", class_="individual_internship"):
        title = item.find("h4", class_="heading_4_5").text.strip()
        company = item.find("a", class_="link_display_like_text").text.strip()
        location = item.find("a", id="location_names").text.strip()
        link = item.find("a", class_="view_detail_button")["href"]
        full_link = f"{INTERNSHALA_URL}{link}"
        internships.append({"title": title, "company": company, "location": location, "link": full_link})

    return internships

# Send Email with Internships List
def send_email(internships):
    subject = "Internships and Jobs List"
    body = "Here are the latest internships and jobs:\n\n"
    for internship in internships:
        body += (
            f"Title: {internship['title']}\n"
            f"Company: {internship['company']}\n"
            f"Location: {internship['location']}\n"
            f"Link: {internship['link']}\n\n"
        )

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Automatically Apply to Internships
def apply_to_internships(driver, internships):
    consent = input("Do you want to apply to these internships? (yes/no): ").lower()
    if consent == "yes":
        for internship in internships:
            driver.get(internship["link"])
            time.sleep(5)  # Wait for the page to load

            try:
                # Click the apply button
                apply_button = driver.find_element(By.ID, "apply_button")
                apply_button.click()
                time.sleep(2)  # Wait for the application page to load

                # Assuming the default resume is already selected
                submit_button = driver.find_element(By.ID, "submit_application")
                submit_button.click()
                time.sleep(2)  # Wait for the application to submit
                print(f"Applied to {internship['title']}")
            except Exception as e:
                print(f"Error applying to {internship['title']}: {e}")

# Main Function
def main():
    # Ask the user for the domain they are interested in
    domain = input("Enter the domain you are seeking internships for (e.g., web development): ")

    # Initialize the WebDriver
    driver = init_driver()
    try:
        # Scrape internships
        internships = scrape_internships(driver, domain)
        print("Scraped Internships:")
        for internship in internships:
            print(
                f"Title: {internship['title']}, "
                f"Company: {internship['company']}, "
                f"Location: {internship['location']}, "
                f"Link: {internship['link']}"
            )

        # Send the list of internships via email
        send_email(internships)

        # Ask the user if they want to apply to the internships
        apply_to_internships(driver, internships)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
