# # import fastapi
# # from fastapi import APIRouter
# # from .functions import AmazonReviewScraper
# # from pydantic import BaseModel
# # scrape_router = APIRouter()

# # class ScrapeRequest(BaseModel):
# #     product_link : str


# # scrape_router.get("/scrape_details")
# # async def get_details(product_link : str):

# #     response = await AmazonReviewScraper(product_link).scrape_and_save()
# #     return response

# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from .amazon_scraper import AmazonReviewScraper
# from .flipkart_scraper import FlipkartReviewScraper
# from .myntra_scraper import MyntraReviewScraper
# from .nykaa_scraper import NykaaReviewScraper
# from .walmart_scraper import WalmartReviewScraper

# scrape_router = APIRouter()

# class ScrapeRequest(BaseModel):
#     product_link: str
#     website: str

# @scrape_router.get("/scrape_details")
# async def get_details(product_link: str, website: str):
#     if website == "amazon":
#         scraper = AmazonReviewScraper(product_link)
#     elif website == "flipkart":
#         scraper = FlipkartReviewScraper(product_link)
#     elif website == "myntra":
#         scraper = MyntraReviewScraper(product_link)
#     elif website == "nykaa":
#         scraper = NykaaReviewScraper(product_link)
#     elif website == "walmart":
#         scraper = WalmartReviewScraper(product_link)
#     else:
#         raise HTTPException(status_code=400, detail="Unsupported website")

#     response = scraper.scrape_and_save()
#     return response

# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from .amazon_scraper import AmazonReviewScraper
# from .flipkart_scraper import FlipkartReviewScraper
# from .myntra_scraper import MyntraReviewScraper

# scrape_router = APIRouter()

# class ScrapeRequest(BaseModel):
#     product_link: str
#     website: str

# @scrape_router.get("/scrape_details")
# async def get_details(product_link: str, website: str):
#     if website == "amazon":
#         scraper = AmazonReviewScraper(product_link)
#     elif website == "flipkart":
#         scraper = FlipkartReviewScraper(product_link)
#     elif website == "myntra":
#         scraper = MyntraReviewScraper(product_link)
#     else:
#         raise HTTPException(status_code=400, detail="Unsupported website")

#     response = scraper.scrape_and_save()
#     return response

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .amazon_scraper import AmazonReviewScraper
from .flipkart_scraper import FlipkartReviewScraper
from .myntra_scraper import MyntraReviewScraper

scrape_router = APIRouter()

class ScrapeRequest(BaseModel):
    product_link: str
    website: str

@scrape_router.get("/scrape_details")
async def get_details(product_link: str, website: str, num_reviews: int = 10):
    if website == "amazon":
        scraper = AmazonReviewScraper(product_link, desired_review_count=num_reviews)
    elif website == "flipkart":
        scraper = FlipkartReviewScraper(product_link, desired_review_count=num_reviews)
    elif website == "myntra":
        scraper = MyntraReviewScraper(product_link, desired_review_count=num_reviews)
    else:
        raise HTTPException(status_code=400, detail="Unsupported website")

    response = scraper.scrape_and_save()
    return response
