"""FastAPI application entry point for CareerGraph AI."""

from fastapi import FastAPI

from careergraph.api.routes.targets import router as target_router

app = FastAPI(title="CareerGraph API")


app.include_router(target_router)


@app.get("/health")
def health() -> dict[str, str]:
    """Return the API health status."""
    return {"status": "healthy"}