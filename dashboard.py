import streamlit as st
import requests
import json

# -----------------------------------------------------------------------------
# Configuration & Constants
# -----------------------------------------------------------------------------
API_URL = "http://127.0.0.1:8000/verify"

# Page Config
st.set_page_config(
    page_title="FactCheck Pro | Enterprise AI Verification",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Custom CSS (Enterprise Styling)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Custom CSS (Enterprise Styling)
# -----------------------------------------------------------------------------
import base64
import os

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Check for background image
bg_image_code = ""
if os.path.exists("background.png"):
    bin_str = get_base64_of_bin_file("background.png")
    bg_image_code = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """

st.markdown(bg_image_code, unsafe_allow_html=True)

st.markdown("""
<style>
    /* Global Fonts & Colors */
    :root {
        --primary-color: #2563eb;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --neutral-color: #6b7280;
        --bg-color: #f9fafb;
        --card-bg: rgba(255, 255, 255, 0.95);
    }

    /* Main Container Background */
    .stApp {
        background: rgb(2,0,36);
        background: radial-gradient(circle, rgba(16,23,54,1) 0%, rgba(5,5,15,1) 100%);
        background-attachment: fixed;
        background-size: cover;
    }
    
    /* If a background image is present, it will be handled by the python script injecting a style block */

    /* Typography */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #f3f4f6; /* Lighter text for dark mode potential, but we are keeping cards white */
    }
    
    /* Force text in cards to be dark */
    .metric-card h1, .metric-card h2, .metric-card h3, .metric-card div {
        color: #111827 !important;
    }
    
    .claim-card h1, .claim-card h2, .claim-card h3, .claim-card div {
        color: #1f2937 !important;
    }

    .stMarkdown p {
        color: #e5e7eb;
    }
    
    /* Fix text inside cards to be readable against white card bg */
    .metric-card .metric-value { color: #111827 !important; }
    .metric-card .metric-label { color: #6b7280 !important; }
    .claim-card .claim-text { color: #1f2937 !important; }
    
    /* Sidebar styling to match dark theme if needed, or keep light */
    [data-testid="stSidebar"] {
        background-color: #f9fafb;
    }

    /* Card Styling */
    .metric-card {
        background-color: var(--card-bg);
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #111827;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--neutral-color);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Claim Card Styling */
    .claim-card {
        background-color: var(--card-bg);
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        border-left-width: 6px;
        transition: transform 0.1s ease-in-out;
        backdrop-filter: blur(5px);
    }
    
    .claim-card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }

    .status-supported { border-left-color: var(--success-color); }
    .status-contradicted { border-left-color: var(--danger-color); }
    .status-unverifiable { border-left-color: var(--warning-color); }

    .claim-text {
        font-size: 1.05rem;
        font-weight: 500;
        margin-bottom: 8px;
        color: #1f2937;
    }

    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .badge-supported { background-color: #d1fae5; color: #065f46; }
    .badge-contradicted { background-color: #fee2e2; color: #991b1b; }
    .badge-unverifiable { background-color: #fef3c7; color: #92400e; }

    /* Hide Default Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Sidebar (Inputs & Controls)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluent/96/000000/checked-user-male.png", width=64)
    st.title("FactCheck Pro")
    st.markdown("**Enterprise Edition v2.4**")
    st.markdown("---")
    
    st.header("1. Source Data")
    uploaded_file = st.file_uploader("Upload Knowledge Base (.txt)", type=["txt"], help="Upload the reference document (ground truth).")
    
    st.header("2. Analysis Target")
    llm_output = st.text_area(
        "Paste LLM Output", 
        height=300, 
        placeholder="Paste the generated text you want to verify here...",
        help="The text generated by an LLM that needs verification against the source."
    )
    
    st.markdown("---")
    
    verify_btn = st.button("Run Verification Analysis", type="primary", use_container_width=True)
    
    if verify_btn and (not uploaded_file or not llm_output):
        st.error("Please provide both a source file and text to verify.")

# -----------------------------------------------------------------------------
# Main Content Area
# -----------------------------------------------------------------------------

# Header
col_header_1, col_header_2 = st.columns([3, 1])
with col_header_1:
    st.title("Verification Dashboard")
    st.markdown("Review and audit AI-generated content against source documentation.")
with col_header_2:
    # Placeholder for status or date
    pass

st.markdown("---")

if verify_btn and uploaded_file and llm_output:
    
    # --- Loading State ---
    with st.spinner("Processing documents and verifying claims..."):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            data = {"llm_output": llm_output}
            
            response = requests.post(API_URL, files=files, data=data) 
            
            if response.status_code == 200:
                result = response.json()
                trust_score = result.get("trust_score", 0)
                claims_data = result.get("results", [])
                
                # --- Metrics Section ---
                st.subheader("Trust Overview")
                
                m1, m2, m3, m4 = st.columns(4)
                
                with m1:
                    # Determine color for trust score
                    score_color = "#10b981" if trust_score >= 80 else "#f59e0b" if trust_score >= 50 else "#ef4444"
                    st.markdown(f"""
                        <div class="metric-card" style="border-top: 4px solid {score_color}">
                            <div class="metric-value" style="color: {score_color}">{trust_score}%</div>
                            <div class="metric-label">Overall Trust Score</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                with m2:
                    count = sum(1 for c in claims_data if c['label'] == 'Supported')
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{count}</div>
                            <div class="metric-label">Supported Claims</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                with m3:
                    count = sum(1 for c in claims_data if c['label'] == 'Contradicted')
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{count}</div>
                            <div class="metric-label">Contradictions</div>
                        </div>
                    """, unsafe_allow_html=True)

                with m4:
                    count = sum(1 for c in claims_data if c['label'] == 'Unverifiable')
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{count}</div>
                            <div class="metric-label">Unverifiable</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # --- Detailed Analysis Section ---
                st.subheader("Detailed Claim Analysis")
                
                if not claims_data:
                    st.info("No claims were extracted for verification.")
                
                for idx, claim in enumerate(claims_data):
                    label = claim['label']
                    status_class = f"status-{label.lower()}"
                    badge_class = f"badge-{label.lower()}"
                    
                    # HTML Card for the primary view
                    st.markdown(f"""
                    <div class="claim-card {status_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span class="badge {badge_class}">{label}</span>
                            <span style="color: #9ca3af; font-size: 0.8rem;">Confidence: {int(claim['similarity'] * 100)}%</span>
                        </div>
                        <div class="claim-text">{claim['claim']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Streamlit Expander for details (Cleanest way to handle interactions)
                    with st.expander(f"View Evidence & Reasoning (Page {claim.get('page', 'N/A')})"):
                        c1, c2 = st.columns([1, 1])
                        
                        with c1:
                            st.markdown("**Reasoning Engine**")
                            st.info(claim['reason'])
                            
                        with c2:
                            st.markdown("**Source Context**")
                            if claim.get('evidence_snippet'):
                                st.caption(f"...{claim['evidence_snippet']}...")
                            else:
                                st.warning("No evidence snippet found.")
                        
                        # Raw Data View (Optional, nice for debugging/auditing)
                        # st.json(claim)

            else:
                st.error(f"Analysis Failed. API returned status code: {response.status_code}")
                st.write(response.text)
                
        except requests.exceptions.ConnectionError:
            st.error("Connection Refused. Please ensure the Verification Backend API is running on port 8000.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

else:
    # Empty State
    st.markdown("""
    <div style="text-align: center; padding: 50px; color: #6b7280;">
        <h3>Ready for Analysis</h3>
        <p>Upload a source document and paste the LLM output in the sidebar to begin.</p>
    </div>
    """, unsafe_allow_html=True)
