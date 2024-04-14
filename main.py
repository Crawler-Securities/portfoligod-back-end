from fastapi.middleware.cors import CORSMiddleware

from src.routes.IBKR import ibkr_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(ibkr_router, prefix="/ibkr")

# # Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or use ["*"] for open access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, log_level="debug", reload=True)
