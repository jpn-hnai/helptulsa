from help_tulsa_vectorizer.main import embed_and_upsert
from help_tulsa_vectorizer.qdrant_client import get_qdrant_client
from help_tulsa_api.routes import COLLECTION


def test_vector_count(qdrant, resources_file):
    count = embed_and_upsert()
    client = get_qdrant_client()
    qcount = client.count(collection_name=COLLECTION).count
    assert qcount == count
