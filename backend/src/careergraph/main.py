"""FastAPI application entry point for CareerGraph AI."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from careergraph.api.routes.evidence import router as evidence_router
from careergraph.api.routes.candidates import router as candidate_router
from careergraph.api.routes.targets import router as target_router

app = FastAPI(title="CareerGraph API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(candidate_router)
app.include_router(target_router)
app.include_router(evidence_router)


@app.get("/health")
def health() -> dict[str, str]:
    """Return the API health status."""
    return {"status": "healthy"}