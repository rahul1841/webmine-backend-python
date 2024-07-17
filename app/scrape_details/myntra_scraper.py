

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# from textblob import TextBlob
# from collections import Counter
# import re
# import os

# class MyntraReviewScraper:
#     def __init__(self, product_link, desired_review_count):
#         self.product_link = product_link
#         self.desired_review_count = desired_review_count
#         # self.path = "C:/Users/91600/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
#         self.current_dir = os.path.dirname(os.path.realpath(__file__))
#         self.path = os.path.join(self.current_dir, '..', '..', 'chromedriver-win64/chromedriver-win64/chromedriver.exe')
#         self.driver = self.init_driver()

#     def init_driver(self):
#         options = webdriver.ChromeOptions()

#         options.add_experimental_option("detach", True)

#         s = Service(self.path)
#         driver = webdriver.Chrome(options=options, service=s)
#         return driver

#     def navigate_to_product(self):
#         self.driver.get(self.product_link)

#     def click_view_all_reviews(self):
#         try:
#             view_all_reviews_button = WebDriverWait(self.driver, 20).until(
#                 EC.element_to_be_clickable(
#                     (By.XPATH, '//a[contains(@class, "detailed-reviews-allReviews") and contains(text(), "View all")]')
#                 )
#             )
#             print("View all reviews button found, clicking...")
#             view_all_reviews_button.click()
#         except Exception as e:
#             print(f"Exception occurred while clicking 'View all reviews': {e}")
#             self.driver.quit()
#             raise

#     def scrape_reviews(self):
#         review_data = {
#             "Reviewer Names": [],
#             "Ratings": [],
#             "Review Dates": [],
#             "Review Headings": [],
#             "Review Texts": [],
#             "Sentiment Scores": []
#         }

#         seen_reviews = set()
#         previous_length = 0  # Track the number of reviews before scrolling

#         while len(review_data["Reviewer Names"]) < self.desired_review_count:
#             reviews = self.driver.find_elements(By.XPATH, '//div[contains(@class, "user-review-userReviewWrapper")]')

#             for review in reviews:
#                 if len(review_data["Reviewer Names"]) >= self.desired_review_count:
#                     break
                
#                 review_text = review.find_element(By.XPATH, './/div[contains(@class, "user-review-reviewTextWrapper")]').text
                
#                 if review_text in seen_reviews:
#                     continue
#                 seen_reviews.add(review_text)

#                 try:
#                     reviewer_name = review.find_element(By.XPATH, './/div[contains(@class, "user-review-left")]/span[1]').text
#                 except:
#                     reviewer_name = "Anonymous"
#                 try:
#                     rating = review.find_element(By.XPATH, './/span[contains(@class, "user-review-starRating")]').text
#                     rating = f"{rating}.0 out of 5 stars"
#                 except:
#                     rating = "Rating not available"
#                 try:
#                     review_date = review.find_element(By.XPATH, './/div[contains(@class, "user-review-left")]/span[2]').text
#                 except:
#                     review_date = "Date not available"
#                 try:
#                     review_heading = review.find_element(By.XPATH, './/a[@data-hook="review-title"]').text
#                 except:
#                     review_heading = "Heading not available"
                
#                 # Perform sentiment analysis for each review
#                 sentiment_score = round(TextBlob(review_text).sentiment.polarity, 2)

#                 review_data["Reviewer Names"].append(reviewer_name)
#                 review_data["Ratings"].append(rating)
#                 review_data["Review Dates"].append(review_date)
#                 review_data["Review Headings"].append(review_heading)
#                 review_data["Review Texts"].append(review_text)
#                 review_data["Sentiment Scores"].append(sentiment_score)

#             if len(review_data["Reviewer Names"]) < self.desired_review_count:
#                 last_review = reviews[-1]
#                 self.driver.execute_script("arguments[0].scrollIntoView();", last_review)
#                 time.sleep(2)  # Adjust the delay as needed to wait for the next reviews to load

#             # Break the loop if no new reviews were loaded (end of the list)
#             current_length = len(review_data["Reviewer Names"])
#             if current_length == previous_length:
#                 print("No more new reviews found, breaking the loop.")
#                 break
#             previous_length = current_length  # Update previous_length

#         return review_data

#     def extract_top_keywords(self, reviews, sentiment_scores, sentiment_type='positive', top_n=10):
#         if sentiment_type == 'positive':
#             filtered_reviews = [reviews[i] for i in range(len(reviews)) if sentiment_scores[i] > 0]
#         else:
#             filtered_reviews = [reviews[i] for i in range(len(reviews)) if sentiment_scores[i] < 0]

#         all_words = ' '.join(filtered_reviews).lower()
#         all_words = re.findall(r'\b\w+\b', all_words)
#         word_counts = Counter(all_words)
#         top_keywords = word_counts.most_common(top_n)
#         return top_keywords

#     def scrape_and_save(self):
#         self.navigate_to_product()
#         self.click_view_all_reviews()
#         review_data = self.scrape_reviews()
#         self.driver.quit()
        
#         # Extract top positive and negative keywords
#         review_texts = review_data["Review Texts"]
#         sentiment_scores = review_data["Sentiment Scores"]
        
#         top_positive_keywords = self.extract_top_keywords(review_texts, sentiment_scores, sentiment_type='positive')
#         top_negative_keywords = self.extract_top_keywords(review_texts, sentiment_scores, sentiment_type='negative')
        
#         # Add top keywords to review data
#         review_data["Top Positive Keywords"] = top_positive_keywords
#         review_data["Top Negative Keywords"] = top_negative_keywords
        
        # return review_data

# Usage example (ensure you have the right URL and replace it here):
# scraper = MyntraReviewScraper('https://www.myntra.com/shirts/campus+sutra/campus-sutra-classic-self-design-spread-collar-casual-shirt/28219632/buy', review_count=20)
# review_data = scraper.scrape_and_save()
# print(review_data)


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from textblob import TextBlob
from collections import Counter
import re
from webdriver_manager.chrome import ChromeDriverManager

class MyntraReviewScraper:
    def __init__(self, product_link, desired_review_count):
        self.product_link = product_link
        self.desired_review_count = desired_review_count
        self.driver = self.init_driver()

    def init_driver(self):
        options = webdriver.ChromeOptions()

        options.add_experimental_option("detach", True)

        # Use webdriver_manager to manage the ChromeDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

    def navigate_to_product(self):
        self.driver.get(self.product_link)

    def click_view_all_reviews(self):
        try:
            view_all_reviews_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//a[contains(@class, "detailed-reviews-allReviews") and contains(text(), "View all")]')
                )
            )
            print("View all reviews button found, clicking...")
            view_all_reviews_button.click()
        except Exception as e:
            print(f"Exception occurred while clicking 'View all reviews': {e}")
            self.driver.quit()
            raise

    def scrape_reviews(self):
        review_data = {
            "Reviewer Names": [],
            "Ratings": [],
            "Review Dates": [],
            "Review Headings": [],
            "Review Texts": [],
            "Sentiment Scores": []
        }

        seen_reviews = set()
        previous_length = 0  # Track the number of reviews before scrolling

        while len(review_data["Reviewer Names"]) < self.desired_review_count:
            reviews = self.driver.find_elements(By.XPATH, '//div[contains(@class, "user-review-userReviewWrapper")]')

            for review in reviews:
                if len(review_data["Reviewer Names"]) >= self.desired_review_count:
                    break
                
                review_text = review.find_element(By.XPATH, './/div[contains(@class, "user-review-reviewTextWrapper")]').text
                
                if review_text in seen_reviews:
                    continue
                seen_reviews.add(review_text)

                try:
                    reviewer_name = review.find_element(By.XPATH, './/div[contains(@class, "user-review-left")]/span[1]').text
                except:
                    reviewer_name = "Anonymous"
                try:
                    rating = review.find_element(By.XPATH, './/span[contains(@class, "user-review-starRating")]').text
                    rating = f"{rating}.0 out of 5 stars"
                except:
                    rating = "Rating not available"
                try:
                    review_date = review.find_element(By.XPATH, './/div[contains(@class, "user-review-left")]/span[2]').text
                except:
                    review_date = "Date not available"
                try:
                    review_heading = review.find_element(By.XPATH, './/a[@data-hook="review-title"]').text
                except:
                    review_heading = "Heading not available"
                
                # Perform sentiment analysis for each review
                sentiment_score = round(TextBlob(review_text).sentiment.polarity, 2)

                review_data["Reviewer Names"].append(reviewer_name)
                review_data["Ratings"].append(rating)
                review_data["Review Dates"].append(review_date)
                review_data["Review Headings"].append(review_heading)
                review_data["Review Texts"].append(review_text)
                review_data["Sentiment Scores"].append(sentiment_score)

            if len(review_data["Reviewer Names"]) < self.desired_review_count:
                last_review = reviews[-1]
                self.driver.execute_script("arguments[0].scrollIntoView();", last_review)
                time.sleep(2)  # Adjust the delay as needed to wait for the next reviews to load

            # Break the loop if no new reviews were loaded (end of the list)
            current_length = len(review_data["Reviewer Names"])
            if current_length == previous_length:
                print("No more new reviews found, breaking the loop.")
                break
            previous_length = current_length  # Update previous_length

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
        self.click_view_all_reviews()
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

