import os
import pickle
import numpy as np
from typing import List, Dict

import faiss

# -----------------------------
# GLOBAL LAZY MODEL (IMPORTANT)
# -----------------------------
_model = None

def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        # small + fast + low memory
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


class VectorStore:
    def __init__(self, persist_dir: str = "./vectorstore"):
        self.persist_dir = persist_dir
        self.index_path = os.path.join(persist_dir, "faiss.index")
        self.metadata_path = os.path.join(persist_dir, "metadata.pkl")

        self.dimension = 384  # MiniLM embedding size
        self.index = None
        self.metadata: List[Dict] = []

        os.makedirs(persist_dir, exist_ok=True)
        self._load_or_create_index()

    # -----------------------------
    # LOAD / INIT INDEX
    # -----------------------------
    def _load_or_create_index(self):
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatIP(self.dimension)
            self.metadata = []

    def _save_index(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)

    # -----------------------------
    # EMBEDDING (LAZY MODEL)
    # -----------------------------
    def _encode(self, texts: List[str]) -> np.ndarray:
        model = get_model()
        embeddings = model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        return np.array(embeddings).astype(np.float32)

    # -----------------------------
    # ADD DOCUMENTS
    # -----------------------------
    def add_documents(self, chunks: List[Dict], filename: str) -> List[int]:
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self._encode(texts)

        start_idx = len(self.metadata)
        self.index.add(embeddings)

        doc_ids = []
        for i, chunk in enumerate(chunks):
            doc_id = start_idx + i
            self.metadata.append({
                **chunk,
                "filename": filename,
                "doc_id": doc_id
            })
            doc_ids.append(doc_id)

        self._save_index()
        return doc_ids

    # -----------------------------
    # SEARCH
    # -----------------------------
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        if self.index.ntotal == 0:
            return []

        query_embedding = self._encode([query])
        actual_k = min(top_k, self.index.ntotal)

        scores, indices = self.index.search(query_embedding, actual_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1 and 0 <= idx < len(self.metadata):
                result = self.metadata[idx].copy()
                result["score"] = float(score)
                results.append(result)

        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    # -----------------------------
    # UTILITIES
    # -----------------------------
    def get_document_count(self) -> int:
        return self.index.ntotal if self.index else 0

    def list_documents(self) -> List[Dict]:
        seen = {}

        for meta in self.metadata:
            fname = meta.get("filename", "unknown")
            if fname not in seen:
                seen[fname] = {"filename": fname, "chunks": 0, "pages": set()}
            seen[fname]["chunks"] += 1
            if meta.get("page"):
                seen[fname]["pages"].add(meta["page"])

        return [
            {
                "filename": fname,
                "chunks": data["chunks"],
                "pages": max(data["pages"]) if data["pages"] else None
            }
            for fname, data in seen.items()
        ]

    def delete_document(self, filename: str) -> bool:
        indices_to_keep = [
            i for i, m in enumerate(self.metadata)
            if m.get("filename") != filename
        ]

        if len(indices_to_keep) == len(self.metadata):
            return False

        self.metadata = [self.metadata[i] for i in indices_to_keep]

        if self.metadata:
            texts = [m["text"] for m in self.metadata]
            embeddings = self._encode(texts)

            self.index = faiss.IndexFlatIP(self.dimension)
            self.index.add(embeddings)
        else:
            self.index = faiss.IndexFlatIP(self.dimension)

        for i, meta in enumerate(self.metadata):
            meta["doc_id"] = i

        self._save_index()
        return True

    def clear_all(self):
        self.index = faiss.IndexFlatIP(self.dimension)
        self.metadata = []
        self._save_index()