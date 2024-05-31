# from fastapi import FastAPI

# app = FastAPI()


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app.app:app", host="127.0.0.1", port=8000, reload=True)


from fastapi import FastAPI
import uvicorn
from app.app import app

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="127.0.0.1", port=8000, reload=True)
