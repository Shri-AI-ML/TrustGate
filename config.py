import torch

# =========================
# DEVICE CONFIGURATION
# =========================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# =========================
# MODEL CONFIG
# =========================

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
NLI_MODEL_NAME = "cross-encoder/nli-deberta-v3-small"

# =========================
# RETRIEVAL CONFIG
# =========================

TOP_K = 3
SIMILARITY_THRESHOLD = 0.55  # Tune later if needed

# =========================
# TRUST SCORING WEIGHTS
# =========================

WEIGHT_SUPPORTED = 1.0
WEIGHT_UNVERIFIABLE = 0.4
WEIGHT_CONTRADICTED_LOW = -0.5
WEIGHT_CONTRADICTED_HIGH = -1.5

# =========================
# TRUST ESCALATION THRESHOLD
# =========================

TRUST_REVIEW_THRESHOLD = 70  # Below this → Manual Review Required


if __name__ == "__main__":
    print("Device:", DEVICE)
