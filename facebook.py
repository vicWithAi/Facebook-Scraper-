import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Path to your chromedriver.exe
chromedriver_path = r'C:\Users\jvicm\fb\chromedriver.exe'

# Facebook login credentials
username = 'victor.maina@boxraft.com'
password = 'Kalejo99@gmail'

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Open Chrome in maximized mode

# Set up ChromeDriver service
service = Service(executable_path=chromedriver_path)

# Initialize WebDriver with service and options
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Visit the Facebook login page
    driver.get('https://www.facebook.com/login')

    # Log in to Facebook
    email_input = driver.find_element(By.ID, 'email')
    password_input = driver.find_element(By.ID, 'pass')
    login_button = driver.find_element(By.NAME, 'login')

    email_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()

    # Wait for the login process to complete
    time.sleep(10)

    # Navigate to the target Facebook page
    driver.get('https://www.facebook.com/Kenyans.co.ke')

    # Scroll down to load posts
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)  # Wait for the page to load

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height or len(driver.find_elements(By.XPATH, '//div[@dir="auto" and contains(@style, "text-align: start;")]')) >= 20:
            break
        last_height = new_height

    # Find posts and extract titles, likes, comments, and shares
    posts = []
    title_elements = driver.find_elements(By.XPATH, '//div[@dir="auto" and contains(@style, "text-align: start;")]')

    for i, title_element in enumerate(title_elements, start=1):
        title = title_element.text

        # Extract likes
        try:
            likes_element = title_element.find_element(By.XPATH, './/following::span[@class="x1e558r4"]')
            likes = likes_element.text
        except:
            likes = "Likes not found"

        # Extract comments
        try:
            comments_element = title_element.find_element(By.XPATH, './/following::span[contains(@class, "x193iq5w")]')
            comments = comments_element.text
        except:
            comments = "Comments not found"

        # Extract shares
        try:
            shares_element = title_element.find_element(By.XPATH, './/following::span[@class="x193iq5w"]')
            shares = shares_element.text
        except:
            shares = "Shares not found"

        # Store the extracted data in the posts list
        posts.append({
            "Title": title,
            "Likes": likes,
            "Comments": comments,
            "Shares": shares
        })

    # Save the extracted data to a JSON file
    with open('facebook_posts.json', 'w') as json_file:
        json.dump(posts, json_file, indent=4)

finally:
    # Make sure to quit the driver
    driver.quit()
