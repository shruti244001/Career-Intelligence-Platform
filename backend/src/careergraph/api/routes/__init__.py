"""CareerGraph API routes."""

from careergraph.api.routes.candidates import router as candidate_router
from careergraph.api.routes.targets import router as target_router

__all__ = ["candidate_router", "target_router"]