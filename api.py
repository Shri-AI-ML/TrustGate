from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

from core.chunking import chunk_pages
from core.claim_extractor import extract_claims
from models.embedding_model import get_embedding_model
from utils.numeric_utils import numeric_match

app = FastAPI(title="AI Fact Verification API")
@app.get("/")
def root():
    return {"message": "AI Fact Verification API Running"}


# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embedding_model = get_embedding_model()


@app.post("/verify")
async def verify(file: UploadFile = File(...), llm_output: str = Form(...)):

    text = (await file.read()).decode("utf-8")

    pages = [{
        "page_number": 1,
        "text": text
    }]

    chunks = chunk_pages(pages)

    # Precompute chunk embeddings
    chunk_embeddings = []
    for chunk in chunks:
        emb = embedding_model.encode(chunk["text"])
        chunk_embeddings.append(emb)

    claims = extract_claims(llm_output)

    results = []

    for claim in claims:

        claim_embedding = embedding_model.encode(claim)

        best_similarity = -1
        best_chunk = None

        for idx, chunk in enumerate(chunks):
            chunk_embedding = chunk_embeddings[idx]

            similarity = np.dot(claim_embedding, chunk_embedding.T) / (
                np.linalg.norm(claim_embedding) * np.linalg.norm(chunk_embedding)
            )

            similarity = similarity.item()

            if similarity > best_similarity:
                best_similarity = similarity
                best_chunk = chunk

        evidence = best_chunk["text"]
        num_check = numeric_match(claim, evidence)

        # Hybrid logic
        if num_check is False:
            final_label = "Contradicted"
            reason = "Numeric mismatch detected."

        elif num_check is True:
            final_label = "Supported"
            reason = "Numeric agreement detected."

        elif best_similarity > 0.50:
            final_label = "Supported"
            reason = f"High semantic similarity ({round(best_similarity,3)})."

        elif 0.35 <= best_similarity <= 0.50:
            final_label = "Unverifiable"
            reason = f"Moderate similarity ({round(best_similarity,3)})."

        else:
            final_label = "Unverifiable"
            reason = f"Low similarity ({round(best_similarity,3)})."

        results.append({
            "claim": claim,
            "label": final_label,
            "similarity": round(best_similarity, 3),
            "reason": reason,
            "evidence_snippet": evidence[:500],
            "page": best_chunk["page_number"]
        })

    supported = sum(1 for r in results if r["label"] == "Supported")
    contradicted = sum(1 for r in results if r["label"] == "Contradicted")
    neutral = sum(1 for r in results if r["label"] == "Unverifiable")

    total = len(results)

    if total > 0:
        trust_score = (
            supported * 1.0 +
            neutral * 0.4 +
            contradicted * 0
        ) / total * 100
    else:
        trust_score = 0

    return {
        "trust_score": round(trust_score, 2),
        "results": results
    }
