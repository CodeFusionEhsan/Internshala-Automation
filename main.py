import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

# Constants
INTERNSHALA_URL = "https://internshala.com"
EMAIL = "YOUR_EMAIL"  # Replace with your email
PASSWORD = "YOUR_PASSWORD"  # Replace with your email password
RECIPIENT_EMAIL = "RECIPIENT_EMAIL"  # Replace with recipient email
WEBDRIVER_PATH = "/path/to/chromedriver"  # Replace with your WebDriver path

# Initialize WebDriver
def init_driver():
    service = Service(executable_path='./chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Scrape Internships and Jobs
def scrape_internships(driver):
    driver.get(INTERNSHALA_URL)
    time.sleep(5)  # Wait for the page to load

    # Search for internships
    search_box = driver.find_element(By.NAME, "keywords")
    search_box.send_keys("Python Developer")
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

    # Parse the page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    internships = []

    for item in soup.find_all("div", class_="internship_meta"):
        title = item.find("h4", class_="heading_4_5").text.strip()
        company = item.find("a", class_="link_display_like_text").text.strip()
        location = item.find("a", id="location_names").text.strip()
        internships.append({"title": title, "company": company, "location": location})

    return internships

# Send Email with Internships List
def send_email(internships):
    subject = "Internships and Jobs List"
    body = "Here are the latest internships and jobs:\n\n"
    for internship in internships:
        body += f"Title: {internship['title']}\nCompany: {internship['company']}\nLocation: {internship['location']}\n\n"

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
def apply_to_internships(driver):
    consent = input("Do you want to apply to these internships? (yes/no): ").lower()
    if consent == "yes":
        for internship in driver.find_elements(By.CLASS_NAME, "internship_meta"):
            apply_button = internship.find_element(By.CLASS_NAME, "apply_button")
            apply_button.click()
            time.sleep(2)  # Wait for the application page to load

            # Assuming the default resume is already selected
            submit_button = driver.find_element(By.ID, "submit_application")
            submit_button.click()
            time.sleep(2)  # Wait for the application to submit
            print(f"Applied to {internship['title']}")

# Main Function
def main():
    driver = init_driver()
    try:
        internships = scrape_internships(driver)
        print("Scraped Internships:")
        for internship in internships:
            print(f"Title: {internship['title']}, Company: {internship['company']}, Location: {internship['location']}")

        send_email(internships)
        apply_to_internships(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
