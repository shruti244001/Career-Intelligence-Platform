"""Firestore client factory."""

from google.cloud import firestore

from careergraph.config.settings import settings


def get_firestore_client() -> firestore.Client:
    """Create a Firestore client using Application Default Credentials."""
    return firestore.Client(
        project=settings.google_cloud_project,
        database="(default)",
    )
