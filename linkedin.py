from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Path to the ChromeDriver executable
driver_path = 'C:\\Users\\jvicm\\fb\\chromedriver.exe'

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Open Chrome in maximized mode

# Create a Service object
service = Service(driver_path)

# Initialize the Chrome driver with the Service object and options
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Navigate to the LinkedIn login page
    driver.get('https://www.linkedin.com/login')

    # Pause to let the page load
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'username')))

    # Enter your email address and password
    driver.find_element(By.ID, 'username').send_keys('yourusername')
    driver.find_element(By.ID, 'password').send_keys('yourpassword')

    # Submit the login form
    driver.find_element(By.CSS_SELECTOR, '.login__form_action_container button').click()

    # Wait for login process to complete
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.nav-item__link')))
    
    # Navigate to the LinkedIn newsletter page
    newsletter_url = 'https://www.linkedin.com/company/kenyans/posts/?feedView=articles'
    driver.get(newsletter_url)

    # Wait for the newsletter page to load
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.t-14.update-components-article__title')))

    # Get the page source
    page_source = driver.page_source

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Debugging output
    print("Page source loaded successfully.")

    # Extract newsletter titles, reactions, comments, and reposts
    posts = []

    # Find all divs with titles
    title_divs = soup.find_all('div', class_='t-14 update-components-article__title break-words t-black t-bold')

    # Debugging output
    print(f"Found {len(title_divs)} title divs.")

    # Find all spans with reactions
    reactions_spans = soup.find_all('span', class_='social-details-social-counts__reactions-count')

    # Debugging output
    print(f"Found {len(reactions_spans)} reactions spans.")

    # Find all spans with comments
    comments_spans = soup.find_all('span', aria_hidden='true', string=lambda text: text and 'comment' in text.lower())

    # Debugging output
    print(f"Found {len(comments_spans)} comments spans.")

    # Find all spans with reposts
    reposts_spans = soup.find_all('span', aria_hidden='true', string=lambda text: text and 'repost' in text.lower())

    # Debugging output
    print(f"Found {len(reposts_spans)} reposts spans.")

    # Extract text from titles
    titles = [div.get_text(strip=True) for div in title_divs]

    # Extract reactions, comments, and reposts
    reactions = [span.get_text(strip=True) for span in reactions_spans]
    comments = [span.get_text(strip=True) for span in comments_spans]
    reposts = [span.get_text(strip=True) for span in reposts_spans]

    # Combine extracted data
    for title, reaction, comment, repost in zip(titles, reactions, comments, reposts):
        posts.append({
            'Title': title,
            'Reactions': reaction,
            'Comments': comment,
            'Reposts': repost
        })

    # Check if posts were found and print them
    if posts:
        for i, post in enumerate(posts, start=1):
            print(f"Post {i}:")
            print(f"Title: {post['Title']}")
            print(f"Reactions: {post['Reactions']}")
            print(f"Comments: {post['Comments']}")
            print(f"Reposts: {post['Reposts']}")
            print()
    else:
        print('Failed to retrieve the newsletter information.')

finally:
    # Make sure to quit the driver
    driver.quit()
