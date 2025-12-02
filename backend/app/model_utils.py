# backend/app/model_utils.py
from sentence_transformers import SentenceTransformer
import numpy as np

_MODEL = None

def get_sentence_transformer(model_name="all-mpnet-base-v2"):
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer(model_name)
    return _MODEL

def get_embeddings_for_list(text_list, model=None):
    if model is None:
        model = get_sentence_transformer()
    return model.encode(text_list, convert_to_numpy=True, show_progress_bar=False)

def cosine_sim(a, b):
    import numpy as np
    if a is None or b is None:
        return 0.0
    # ensure 2d
    if a.ndim == 1:
        a = a.reshape(1, -1)
    if b.ndim == 1:
        b = b.reshape(1, -1)
    a_norm = a / (np.linalg.norm(a, axis=1, keepdims=True) + 1e-9)
    b_norm = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-9)
    return float(np.dot(a_norm, b_norm.T).max())
