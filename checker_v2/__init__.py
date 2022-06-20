from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")


def similarity_rating(first, second):
    embeddings = model.encode([first, second])
    embeddings.shape

    comp = list(cosine_similarity(
        [embeddings[0]],
        embeddings[1:]
    ))

    return comp[0][0]
