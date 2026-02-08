"""
Diligence-Zero: High-Agency Agentic System for Biotech Asset Analysis
Beautiful Streamlit UI with Real-Time Thought Trace Visualization
"""

import streamlit as st
from backend import DiligenceEngine, ScientificAsset
import time
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Diligence-Zero | Agentic Biotech Analysis",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful, modern design
st.markdown("""
<style>
    /* Minimal styling for cleaner layout */
    
    /* Headers */
    h1 {
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    h2, h3 {
        font-weight: 600;
        margin-top: 1rem;
    }
    
    /* Thought trace styling (Clean Light Mode) */
    .thought-trace {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: 'Monaco', 'Courier New', monospace;
        font-size: 0.85rem;
        color: #334155;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .thought-agent-a { color: #2563eb; font-weight: 600; }
    .thought-agent-b { color: #7c3aed; font-weight: 600; }
    .thought-supervisor { color: #059669; font-weight: 600; }
    .thought-system { color: #d97706; font-weight: 600; }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
    }
    
    /* Metrics containers */
    [data-testid="stMetricValue"] {
        color: #4f46e5 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state (retaining session state for analysis results)
if 'engine' not in st.session_state:
    st.session_state.engine = None
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'thought_trace' not in st.session_state:
    st.session_state.thought_trace = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv("GROQ_API_KEY", "")

# Sidebar Configuration
# Only show API key config if not set in environment or if explicitly requested
api_key_env = os.getenv("GROQ_API_KEY")
if not api_key_env:
    with st.sidebar:
        st.markdown("## ⚙️ Setup")
        api_key_input = st.text_input(
            "Groq API Key",
            value=st.session_state.api_key,
            type="password",
            help="Enter your Groq API key for LLM inference"
        )
        if api_key_input != st.session_state.api_key:
            st.session_state.api_key = api_key_input
            st.session_state.engine = None
        else:
            st.warning("⚠️ API Key not found in .env file")
else:
    # Key found in env, hide sidebar config by default
    st.session_state.api_key = api_key_env

# Main Content Area
st.title("🧬 Diligence-Zero")
st.markdown("### High-Agency Agentic System for Biotech Asset Analysis")
st.markdown("*Reduces manual asset diligence from hours to seconds by identifying \"Confidence Gaps\"*")

st.markdown("---")

from backend import DiligenceEngine, ScientificAsset, extract_text_from_pdf

# ... (rest of imports) ...

# ... (omitted config and styling code) ...

# Document Input Section (Main Page)
doc1_content = None
doc2_content = None

with st.expander("📄 Source Documents (Upload PDFs)", expanded=not st.session_state.analysis_result):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Document 1")
        doc1_type = st.selectbox(
            "Type",
            ["Press Release", "Clinical Trial Report", "FDA Submission", "Patent Filing", "Scientific Publication"],
            key="doc1_type"
        )
        uploaded_file1 = st.file_uploader("Upload PDF", type=['pdf'], key="doc1_upload")
        if uploaded_file1:
            try:
                doc1_content = extract_text_from_pdf(uploaded_file1)
                st.success(f"✅ Loaded: {uploaded_file1.name}")
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
    
    with col2:
        st.markdown("#### Document 2")
        doc2_type = st.selectbox(
            "Type",
            ["Clinical Trial Report", "FDA Submission", "Press Release", "Patent Filing", "Scientific Publication"],
            key="doc2_type"
        )
        uploaded_file2 = st.file_uploader("Upload PDF", type=['pdf'], key="doc2_upload")
        if uploaded_file2:
            try:
                doc2_content = extract_text_from_pdf(uploaded_file2)
                st.success(f"✅ Loaded: {uploaded_file2.name}")
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
    
    # Analyze button centered
    st.markdown("<br>", unsafe_allow_html=True)
    col_centered = st.columns([1, 2, 1])
    with col_centered[1]:
        analyze_button = st.button("🚀 Analyzing Conflicting Documents", use_container_width=True)


# Run analysis when button is clicked
if analyze_button:
    if not st.session_state.api_key:
        st.error("❌ Please ensure your Groq API Key is configured in .env")
    elif not doc1_content or not doc2_content:
        st.error("❌ Please upload both PDF documents to proceed.")
    else:
        # Initialize or get engine
        if st.session_state.engine is None:
            try:
                st.session_state.engine = DiligenceEngine(api_key=st.session_state.api_key)
                st.toast("✅ Diligence Engine initialized!", icon="🚀")
            except Exception as e:
                st.error(f"❌ Failed to initialize engine: {str(e)}")
                st.stop()
        
        # Progress indicator
        with st.spinner("🔄 Reading PDFs and initializing multi-agent debate..."):
            try:
                # Run the analysis using extracted content
                start_time = time.time()
                asset, trace = st.session_state.engine.process_dual_documents(
                    doc1_content, doc1_type,
                    doc2_content, doc2_type
                )

                end_time = time.time()
                
                st.session_state.analysis_result = asset
                st.session_state.thought_trace = trace
                st.session_state.analysis_time = end_time - start_time
                
                st.success(f"✅ Analysis complete in {st.session_state.analysis_time:.2f} seconds!")
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.stop()

# Display results if available
if st.session_state.analysis_result:
    asset = st.session_state.analysis_result
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Confidence Score",
            f"{asset.confidence_score:.0%}",
            delta=None
        )
    
    with col2:
        st.metric(
            "Conflicts Detected",
            len(asset.conflicts_found),
            delta=None,
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            "Clinical Phase",
            asset.clinical_phase,
            delta=None
        )
    
    with col4:
        if hasattr(st.session_state, 'analysis_time'):
            st.metric(
                "Analysis Time",
                f"{st.session_state.analysis_time:.1f}s",
                delta=None
            )
    
    st.markdown("---")
    
    # Two-column layout: Asset Profile (Left) and Thought Trace (Right)
    left_col, right_col = st.columns([6, 4])
    
    with left_col:
        st.markdown("## 📊 Verified Asset Profile")
        st.markdown("**Ground Truth** extracted from multi-source analysis")
        
        # Display asset details in a structured way
        st.markdown("### 🧪 Drug Information")
        profile_col1, profile_col2 = st.columns(2)
        
        with profile_col1:
            st.markdown(f"**Drug Name:** `{asset.drug_name}`")
            st.markdown(f"**Molecule Type:** `{asset.molecule_type}`")
        
        with profile_col2:
            st.markdown(f"**Clinical Phase:** `{asset.clinical_phase}`")
            st.markdown(f"**Confidence:** `{asset.confidence_score:.1%}`")
        
        st.markdown("### ⚠️ Safety Profile")
        st.markdown(f"**Primary Toxicity Finding:**")
        st.info(asset.primary_toxicity_finding)
        
        # Conflicts section
        if asset.conflicts_found:
            st.markdown("### 🔍 Conflicts Detected")
            for i, conflict in enumerate(asset.conflicts_found, 1):
                st.warning(f"**Conflict {i}:** {conflict}")
        else:
            st.success("✅ No conflicts detected - sources are in perfect agreement!")
        
        # Source summary
        if asset.source_summary:
            st.markdown("### 📝 Reconciliation Summary")
            st.markdown(asset.source_summary)
        
        # Raw JSON export
        with st.expander("🔧 View Raw JSON"):
            st.json(asset.model_dump())
    
    with right_col:
        st.markdown("## 🧠 Agent Thought Trace")
        st.markdown("**Live reasoning process** for observability")
        
        # Display thought trace with color coding
        trace_html = '<div class="thought-trace">'
        
        for thought in st.session_state.thought_trace:
            # Color code based on agent
            if "[Agent A]" in thought:
                trace_html += f'<div><span class="thought-agent-a">[Agent A]</span>{thought.split("]", 1)[1]}</div>'
            elif "[Agent B]" in thought:
                trace_html += f'<div><span class="thought-agent-b">[Agent B]</span>{thought.split("]", 1)[1]}</div>'
            elif "[Supervisor]" in thought:
                trace_html += f'<div><span class="thought-supervisor">[Supervisor]</span>{thought.split("]", 1)[1]}</div>'
            elif "[System]" in thought:
                trace_html += f'<div><span class="thought-system">[System]</span>{thought.split("]", 1)[1]}</div>'
            else:
                trace_html += f'<div>{thought}</div>'
        
        trace_html += '</div>'
        
        st.markdown(trace_html, unsafe_allow_html=True)
        
        # Download trace button
        trace_text = "\n".join(st.session_state.thought_trace)
        st.download_button(
            label="💾 Download Thought Trace",
            data=trace_text,
            file_name=f"thought_trace_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )


