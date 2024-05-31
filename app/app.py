# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from .scrape_details.routes import scrape_router
# from .scrape_details.functions import AmazonReviewScraper
# app = FastAPI()

# # CORS Configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # Update this with the origin of your frontend application
#     allow_credentials=True,
#     allow_methods=["GET", "POST"],
#     allow_headers=["*"],
# )

# @app.get("/scrape_details")
# async def get_details(product_link : str):

#     response =  AmazonReviewScraper(product_link).scrape_and_save()
#     return response

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the FastAPI application!"}

# # from fastapi import FastAPI
# # app = FastAPI()
# # @app.get("/")
# # async def root():
# #     return {"message": "Hello World"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .scrape_details.routes import scrape_router

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Update this with the origin of your frontend application
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(scrape_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}
