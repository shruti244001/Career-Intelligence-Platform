"""FastAPI application entry point for CareerGraph AI."""

from fastapi import FastAPI

app = FastAPI(title="CareerGraph API")


@app.get("/health")
def health() -> dict[str, str]:
    """Return the API health status."""
    return {"status": "healthy"}

