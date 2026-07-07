from fastapi import FastAPI

app = FastAPI(
    title="Trading OS Backend",
    version="0.1.0"
)


@app.get("/")
def root():
    return {"message": "RetailFish API"}


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }