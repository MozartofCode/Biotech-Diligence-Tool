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
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --bg-dark: #0f172a;
        --bg-card: #1e293b;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Headers */
    h1 {
        color: #f8fafc;
        font-weight: 700;
        font-size: 2.5rem !important;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: #e2e8f0;
        font-weight: 600;
        font-size: 1.75rem !important;
        margin-top: 1rem;
    }
    
    h3 {
        color: #cbd5e1;
        font-weight: 500;
        font-size: 1.25rem !important;
    }
    
    /* Card-like containers */
    .element-container {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 12px;
        padding: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    [data-testid="stSidebar"] .element-container {
        background: rgba(15, 23, 42, 0.6);
    }
    
    /* Text areas */
    .stTextArea textarea {
        background: #0f172a !important;
        border: 2px solid #334155 !important;
        border-radius: 8px !important;
        color: #f8fafc !important;
        font-family: 'Monaco', 'Courier New', monospace !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(99, 102, 241, 0.3) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #6366f1 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 500 !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        background: #0f172a;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #334155;
    }
    
    /* Success/Warning/Error boxes */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border-left: 4px solid #10b981 !important;
        color: #10b981 !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        border-left: 4px solid #f59e0b !important;
        color: #f59e0b !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border-left: 4px solid #ef4444 !important;
        color: #ef4444 !important;
    }
    
    /* Thought trace styling */
    .thought-trace {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: 'Monaco', 'Courier New', monospace;
        font-size: 0.85rem;
        color: #e2e8f0;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .thought-trace::-webkit-scrollbar {
        width: 8px;
    }
    
    .thought-trace::-webkit-scrollbar-track {
        background: #1e293b;
        border-radius: 4px;
    }
    
    .thought-trace::-webkit-scrollbar-thumb {
        background: #6366f1;
        border-radius: 4px;
    }
    
    .thought-agent-a {
        color: #3b82f6;
        font-weight: 600;
    }
    
    .thought-agent-b {
        color: #8b5cf6;
        font-weight: 600;
    }
    
    .thought-supervisor {
        color: #10b981;
        font-weight: 600;
    }
    
    .thought-system {
        color: #f59e0b;
        font-weight: 600;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.8) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        color: #e2e8f0 !important;
    }
    
    /* Input field */
    input {
        background: #0f172a !important;
        border: 2px solid #334155 !important;
        border-radius: 8px !important;
        color: #f8fafc !important;
    }
    
    input:focus {
        border-color: #6366f1 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'engine' not in st.session_state:
    st.session_state.engine = None
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'thought_trace' not in st.session_state:
    st.session_state.thought_trace = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv("GROQ_API_KEY", "")

# Sidebar Configuration
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    # API Key input
    api_key_input = st.text_input(
        "Groq API Key",
        value=st.session_state.api_key,
        type="password",
        help="Enter your Groq API key for LLM inference"
    )
    
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
        st.session_state.engine = None  # Reset engine on key change
    
    st.markdown("---")
    
    # Source Data Inputs
    st.markdown("## 📄 Source Documents")
    
    doc1_type = st.selectbox(
        "Document 1 Type",
        ["Press Release", "Clinical Trial Report", "FDA Submission", "Patent Filing", "Scientific Publication"],
        key="doc1_type"
    )
    
    doc1_text = st.text_area(
        f"{doc1_type} Content",
        height=200,
        placeholder="Paste the first source document here...",
        help="Enter the text from your first source document",
        key="doc1_text"
    )
    
    st.markdown("---")
    
    doc2_type = st.selectbox(
        "Document 2 Type",
        ["Clinical Trial Report", "FDA Submission", "Press Release", "Patent Filing", "Scientific Publication"],
        key="doc2_type"
    )
    
    doc2_text = st.text_area(
        f"{doc2_type} Content",
        height=200,
        placeholder="Paste the second source document here...",
        help="Enter the text from your second source document",
        key="doc2_text"
    )
    
    st.markdown("---")
    
    # Analyze button
    analyze_button = st.button("🚀 Run Analysis", use_container_width=True)
    
    # About section
    with st.expander("ℹ️ About Diligence-Zero"):
        st.markdown("""
        **Diligence-Zero** is a high-agency agentic system that:
        
        - 🔍 Ingests conflicting scientific data
        - 🤖 Uses multi-agent debate pattern
        - 🧠 Performs deep cross-document reasoning
        - ✅ Produces unified "Ground Truth" profiles
        - 📊 Shows complete reasoning audit trail
        
        Built with Groq LPU for maximum inference speed.
        """)

# Main Content Area
st.title("🧬 Diligence-Zero")
st.markdown("**High-Agency Agentic System for Biotech Asset Analysis**")
st.markdown("*Reduces manual asset diligence from hours to seconds by identifying \"Confidence Gaps\"*")

st.markdown("---")

# Run analysis when button is clicked
if analyze_button:
    if not st.session_state.api_key:
        st.error("❌ Please enter your Groq API Key in the sidebar configuration.")
    elif not doc1_text or not doc2_text:
        st.error("❌ Please provide both source documents in the sidebar.")
    else:
        # Initialize or get engine
        if st.session_state.engine is None:
            try:
                st.session_state.engine = DiligenceEngine(api_key=st.session_state.api_key)
                st.success("✅ Diligence Engine initialized successfully!")
            except Exception as e:
                st.error(f"❌ Failed to initialize engine: {str(e)}")
                st.stop()
        
        # Progress indicator
        with st.spinner("🔄 Analyzing documents with multi-agent system..."):
            try:
                # Run the analysis
                start_time = time.time()
                asset, trace = st.session_state.engine.process_dual_documents(
                    doc1_text, doc1_type,
                    doc2_text, doc2_type
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

else:
    # Welcome screen when no analysis has been run
    st.markdown("## 👋 Welcome to Diligence-Zero")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🔍 Step 1")
        st.markdown("Configure your Groq API key in the sidebar")
    
    with col2:
        st.markdown("### 📄 Step 2")
        st.markdown("Paste two conflicting scientific documents")
    
    with col3:
        st.markdown("### 🚀 Step 3")
        st.markdown("Click 'Run Analysis' and watch the magic happen")
    
    st.markdown("---")
    
    # Example use case
    st.markdown("## 💡 Example Use Cases")
    
    example_col1, example_col2 = st.columns(2)
    
    with example_col1:
        st.markdown("""
        **🧪 Scenario 1: Press Release vs Clinical Trial**
        - Document 1: Company press release announcing "excellent safety"
        - Document 2: Actual clinical trial report showing adverse events
        - **Result**: Agent identifies discrepancy and provides ground truth
        """)
    
    with example_col2:
        st.markdown("""
        **📊 Scenario 2: FDA vs Patent Filing**
        - Document 1: FDA submission with Phase 2 designation
        - Document 2: Patent filing claiming Phase 3 readiness
        - **Result**: Supervisor reconciles timeline and flags conflict
        """)
    
    st.info("💡 **Pro Tip**: The system works best with documents that contain specific scientific parameters like drug names, clinical phases, and safety data.")

# Footer
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("**Built with:**")
    st.markdown("🚀 Groq LPU (`llama-3.3-70b-versatile`)")

with footer_col2:
    st.markdown("**Architecture:**")
    st.markdown("🤖 Multi-Agent Debate Pattern")

with footer_col3:
    st.markdown("**For:**")
    st.markdown("🏢 Convexia (YC S25)")
