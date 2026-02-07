import numpy as np

from core.ingestion import extract_text_from_txt
from core.chunking import chunk_pages
from core.claim_extractor import extract_claims
from models.embedding_model import get_embedding_model
from utils.numeric_utils import numeric_match, extract_numbers


# ============================================
# LOAD DOCUMENT
# ============================================

pages = extract_text_from_txt("data/raw_docs/oncology_case.txt")
print("Pages extracted:", len(pages))

chunks = chunk_pages(pages)
print("Chunks created:", len(chunks))


# ============================================
# LLM OUTPUT (Oncology Test)
# ============================================

llm_output = """
The patient is 45 years old.
The tumor size is 3 cm.
The patient has Stage III cancer.
The white blood cell count is 6000 cells/mcL.
"""

claims = extract_claims(llm_output)

print("\nClaims list:", claims)


# ============================================
# LOAD EMBEDDING MODEL
# ============================================

embedding_model = get_embedding_model()

# Precompute chunk embeddings
chunk_embeddings = []
for chunk in chunks:
    emb = embedding_model.encode(chunk["text"])
    chunk_embeddings.append(emb)


# ============================================
# VERIFICATION ENGINE
# ============================================

results = []

for claim in claims:
    print("\n==========================")
    print("Checking claim:", claim)

    claim_embedding = embedding_model.encode(claim)

    best_similarity = -1
    best_chunk = None

    # Find best chunk
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

    print("Best similarity:", round(best_similarity, 3))
    print("Evidence snippet:", evidence[:200])

    # 🔎 DEBUG NUMERIC EXTRACTION
    print("Claim numbers:", extract_numbers(claim))
    print("Evidence numbers:", extract_numbers(evidence))

    # ----------------------------------------
    # HYBRID DECISION LOGIC
    # ----------------------------------------

    num_check = numeric_match(claim, evidence)

    # Numeric contradiction
    if num_check is False:
        final_label = "Contradicted"
        reason = "Numeric mismatch detected between claim and source document."

    # Numeric agreement boost
    elif num_check is True and best_similarity > 0.30:
        final_label = "Supported"
        reason = (
            f"Numeric agreement detected and semantic similarity "
            f"({round(best_similarity,3)}) above minimal threshold."
        )

    # Strong semantic similarity
    elif best_similarity > 0.50:
        final_label = "Supported"
        reason = (
            f"High semantic similarity ({round(best_similarity,3)} > 0.50 threshold)."
        )

    # Moderate similarity
    elif 0.35 <= best_similarity <= 0.50:
        final_label = "Unverifiable"
        reason = (
            f"Moderate similarity ({round(best_similarity,3)}). "
            "Evidence insufficient for confirmation."
        )

    # Low similarity
    else:
        final_label = "Unverifiable"
        reason = (
            f"Low similarity ({round(best_similarity,3)}). "
            "No sufficient evidence found in source document."
        )

    print("Final Label:", final_label)
    print("Reason:", reason)
    print("Source Page:", best_chunk["page_number"])

    results.append({
        "claim": claim,
        "label": final_label,
        "similarity": best_similarity,
        "reason": reason,
        "page": best_chunk["page_number"],
        "evidence_snippet": evidence[:300]
    })


# ============================================
# TRUST SCORE
# ============================================

supported = sum(1 for r in results if r["label"] == "Supported")
contradicted = sum(1 for r in results if r["label"] == "Contradicted")
neutral = sum(1 for r in results if r["label"] == "Unverifiable")

total = len(results)

if total == 0:
    trust_score = 0
else:
    trust_score = (
        supported * 1.0 +
        neutral * 0.4 +
        contradicted * 0
    ) / total * 100

print("\n==========================")
print("Trust Score:", round(trust_score, 2), "%")
