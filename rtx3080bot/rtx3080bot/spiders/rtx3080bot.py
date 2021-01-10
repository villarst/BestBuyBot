import scrapy
import time
from selenium import webdriver
from scrapy.http import Request
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# To run the program type into the terminal "cd rtx3080bot" then type "scrapy crawl run" with 'run' being the name.
# Quick note to be mentioned here, you must have Firefox installed and grab the profile by entering "about:profiles"
# and copying where the firefox profile is located.


class BestbuySpider(scrapy.Spider):
    name = "run"
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/43.0.2357.130 Safari/537.36 "
    # Enter Your Product URL Here.
    start_urls = [
        # Logging into
        # This would be the link from best buy of the item you wish to buy.
        "LINK TO URL BESTBUY PAGE", ]

    def parse(self, response):
        #  Finding Product Status.
        try:
            product = response.xpath(
                "//*[@class='btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button']")
            if product:
                print(f"\nProduct is Currently: Available.\n")
            else:
                print("\nProduct is Out of Stock.\n")
        except NoSuchElementException:
            pass

        if product:
            print("\nFound 1 item to add to cart.\n")

            # Booting WebDriver.
            # Insert Firefox Profile below.
            profile = webdriver.FirefoxProfile(r'!!!!address_to_FireFoxProfile!!!!')
            driver = webdriver.Firefox(profile, executable_path=GeckoDriverManager().install())

            # Starting Webpage.
            driver.get(response.url)
            time.sleep(1)

            # Click Add to Cart.
            print("\nClicking Add To Cart Button.\n")
            driver.find_element_by_xpath(
                "//*[@class='btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button']").click()
            time.sleep(1)

            # Click Cart.
            print("\nGoing to Shopping Cart.\n")
            driver.get("https://www.bestbuy.com/cart")
            time.sleep(1)

            # Clicks the bubble for "FREE Shipping to..."
            print("\nClicking the FREE Shipping Bubble.\n")
            driver.find_element_by_xpath("//*[starts-with(@id,'fulfillment-shipping-')]").click()

            # Go to checkout manually.
            print("\nGoing to Checkout Manually.\n")
            driver.get("https://www.bestbuy.com/checkout/r/fast-track")

            # Giving Website Time To Login.
            print("\nGiving Website Time To Login..\n")
            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@class='btn btn-lg btn-block btn-primary button__fast-track']")))
            time.sleep(3)

            # CVV Number Input.
            print("\nInputing CVV Number.\n")
            try:
                security_code = driver.find_element_by_id("credit-card-cvv")
                time.sleep(5)
                security_code.send_keys("###")  # You can enter your CVV number here.
            except NoSuchElementException:
                pass

            # Complete Purchase Below.
            print("\nBuying Product.\n")
            driver.find_element_by_xpath("//*[@class='btn btn-lg btn-block btn-primary button__fast-track']").click()

            print("\nBot has Completed Checkout.\n")
            time.sleep(1800)

        else:
            print("\nRetrying Bot In 2 Seconds.\n")
            time.sleep(2)
            yield Request(response.url, callback=self.parse, dont_filter=True)