from flask import Flask, render_template, request
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_price', methods=['POST'])
def check_price():
    product_url = request.form['product_url']
    target_price = float(request.form['target_price'])

    def check_price_and_order():
        # Specify the path to the ChromeDriver executable
        chrome_driver_path = '/path/to/chromedriver'

        # Configure Chrome options
        chrome_options = Options()
        chrome_service = Service(chrome_driver_path)

        # Initialize the WebDriver
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        while True:
            driver.get(product_url)
            time.sleep(5)  # Wait for the page to load

            # Find the price element (you may need to adjust the selector)
            price_element = driver.find_element(By.CSS_SELECTOR, '._30jeq3._16Jk6d')
            price = float(price_element.text.replace('₹', '').replace(',', ''))

            if price <= target_price:
                # Add to cart
                add_to_cart_button = driver.find_element(By.CSS_SELECTOR, '._2KpZ6l._2U9uOA._3v1-ww')
                add_to_cart_button.click()
                time.sleep(2)

                # Proceed to checkout
                checkout_button = driver.find_element(By.CSS_SELECTOR, '._2KpZ6l._2ObVJD._3AWRsL')
                checkout_button.click()
                time.sleep(2)

                # Log in (if not already logged in)
                email_input = driver.find_element(By.CSS_SELECTOR, '._2IX_2-.VJZDxU')
                email_input.send_keys('your-email@example.com')
                password_input = driver.find_element(By.CSS_SELECTOR, '._2IX_2-._3mctLh.VJZDxU')
                password_input.send_keys('your-password')
                login_button = driver.find_element(By.CSS_SELECTOR, '._2KpZ6l._2HKlqd._3AWRsL')
                login_button.click()
                time.sleep(5)

                # Confirm order
                confirm_button = driver.find_element(By.CSS_SELECTOR, '._2KpZ6l._2ObVJD._3AWRsL')
                confirm_button.click()
                driver.quit()
                return "Order placed successfully!"
            else:
                time.sleep(60)  # Check the price every minute

    result = check_price_and_order()
    return result

if __name__ == "__main__":
    app.run(debug=True)
