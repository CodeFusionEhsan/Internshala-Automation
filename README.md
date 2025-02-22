Explanation:
Web Scraping:

The script uses Selenium to navigate Internshala and BeautifulSoup to parse the HTML content.

It searches for internships related to "Python Developer" and extracts details like title, company, and location.

Email Automation:

The script sends an email with the list of internships using the smtplib library.

Auto-Applying:

The script asks for user consent before applying to internships.

It automatically clicks the "Apply" button and submits the application using the default resume.

Notes:
Ethical Use: Always respect the terms of service of the website. Automating actions like applying to internships may violate Internshala's policies.

Error Handling: Add more robust error handling for production use.

Security: Avoid hardcoding sensitive information like passwords. Use environment variables or a secure vault.
