

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from textblob import TextBlob
from collections import Counter
import re
import os

class FlipkartReviewScraper:
    def __init__(self, product_link, desired_review_count):
        self.product_link = product_link
        self.desired_review_count = desired_review_count
        # self.path = "C:/Users/91600/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.join(self.current_dir, '..', '..', 'chromedriver-win64/chromedriver-win64/chromedriver.exe')
        self.driver = self.init_driver()
        self.scraped_reviews = set()

    def init_driver(self):
        options = webdriver.ChromeOptions()

        options.add_experimental_option("detach", True)

        # options.add_argument("--headless")  # Run Chrome in headless mode
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--window-size=1920x1080")
        # options.add_argument("--remote-debugging-port=9222")
        # options.add_argument("--disable-extensions")
        # options.add_argument("--proxy-server='direct://'")
        # options.add_argument("--proxy-bypass-list=*")
        # options.add_argument("--start-maximized")
        # options.add_argument("--disable-infobars")
        # options.add_argument("--disable-notifications")
        # options.add_argument("--disable-popup-blocking")

        s = Service(self.path)
        driver = webdriver.Chrome(options=options, service=s)
        return driver

    def navigate_to_product(self):
        self.driver.get(self.product_link)
        time.sleep(5)  # Wait for the page to load completely

    def click_see_more_button(self):
        see_more_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="_23J90q RcXBOT"]'))
        )
        see_more_button.click()
        time.sleep(5)  # Wait for the reviews to load

    def scrape_reviews(self):
        review_data = {
            "Reviewer Names": [],
            "Ratings": [],
            "Review Dates": [],
            "Review Headings": [],
            "Review Texts": [],
            "Sentiment Scores": []
        }

        while len(review_data["Reviewer Names"]) < self.desired_review_count:
            reviews = self.driver.find_elements(By.XPATH, '//div[@class="col EPCmJX Ma1fCG"]')

            for review in reviews:
                if len(review_data["Reviewer Names"]) >= self.desired_review_count:
                    break

                try:
                    reviewer_name = review.find_element(By.XPATH, './/p[@class="_2NsDsF AwS1CA"]').text
                except:
                    reviewer_name = "Anonymous"
                try:
                    rating = review.find_element(By.XPATH, './/div[@class="XQDdHH Ga3i8K"]').text
                    rating = f"{rating}.0 out of 5 stars"
                except:
                    rating = "Rating not available"
                try:
                    review_date = review.find_element(By.XPATH, './/p[@class="_2NsDsF"]').text
                except:
                    review_date = "Date not available"
                try:
                    review_heading = review.find_element(By.XPATH, './/p[@class="z9E0IG"]').text
                except:
                    review_heading = "Heading not available"
                try:
                    review_text_element = review.find_element(By.XPATH, './/div[@class="ZmyHeo"]')
                    review_text = review_text_element.text.split('READ MORE')[0].strip()
                except:
                    review_text = "Review text not available"

                review_tuple = (reviewer_name, rating, review_date, review_heading, review_text)
                if review_tuple not in self.scraped_reviews:
                    self.scraped_reviews.add(review_tuple)
                    review_data["Reviewer Names"].append(reviewer_name)
                    review_data["Ratings"].append(rating)
                    review_data["Review Dates"].append(review_date)
                    review_data["Review Headings"].append(review_heading)
                    review_data["Review Texts"].append(review_text)

                    # Perform sentiment analysis for each review
                    sentiment_score = round(TextBlob(review_text).sentiment.polarity, 2)
                    review_data["Sentiment Scores"].append(sentiment_score)

            if len(review_data["Reviewer Names"]) < self.desired_review_count:
                try:
                    next_page_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//a[@class="_9QVEpD"]//span[text()="Next"]'))
                    )
                    next_page_button.click()
                    time.sleep(5)  # Wait for the next page to load
                except:
                    break  # If next button is not found or clickable, break the loop

        return review_data

    def extract_top_keywords(self, reviews, sentiment_scores, sentiment_type='positive', top_n=10):
        if sentiment_type == 'positive':
            filtered_reviews = [reviews[i] for i in range(len(reviews)) if sentiment_scores[i] > 0]
        else:
            filtered_reviews = [reviews[i] for i in range(len(reviews)) if sentiment_scores[i] < 0]

        all_words = ' '.join(filtered_reviews).lower()
        all_words = re.findall(r'\b\w+\b', all_words)
        word_counts = Counter(all_words)
        top_keywords = word_counts.most_common(top_n)
        return top_keywords

    def scrape_and_save(self):
        self.navigate_to_product()
        self.click_see_more_button()
        review_data = self.scrape_reviews()
        self.driver.quit()
        
        # Extract top positive and negative keywords
        review_texts = review_data["Review Texts"]
        sentiment_scores = review_data["Sentiment Scores"]
        
        top_positive_keywords = self.extract_top_keywords(review_texts, sentiment_scores, sentiment_type='positive')
        top_negative_keywords = self.extract_top_keywords(review_texts, sentiment_scores, sentiment_type='negative')
        
        # Add top keywords to review data
        review_data["Top Positive Keywords"] = top_positive_keywords
        review_data["Top Negative Keywords"] = top_negative_keywords
        
        return review_data

# Example usage
# product_link = 'https://www.flipkart.com/noise-colorfit-icon-2-1-8-display-bluetooth-calling-ai-voice-assistant-smartwatch/product-reviews/itm9d8957f65c72e?pid=SMWGEH7WC8F4VKKZ&lid=LSTSMWGEH7WC8F4VKKZ6TOWMG&marketplace=FLIPKART'  # Replace with actual product link
# scraper = FlipkartReviewScraper(product_link)
# reviews = scraper.scrape_and_save()
# print(reviews)

