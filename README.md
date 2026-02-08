# 🧬 Diligence-Zero

> **High-Agency Agentic System:** Reduces manual biotech asset diligence from hours to seconds by identifying "Confidence Gaps" between conflicting scientific sources.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Groq](https://img.shields.io/badge/Groq-LPU-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🎯 The Hook

**Diligence-Zero** is a demonstration of a "High-Agency" multi-agent system that ingests conflicting scientific drug data from multiple sources, performs deep cross-document reasoning using Groq's LPU, and produces a unified "Ground Truth" asset profile with a complete audit trail. Built for Convexia (YC S25) to showcase the power of transparent, observable AI reasoning in biotech diligence.

---

## ✨ Key Features

- **🤖 Multi-Agent Debate Pattern**: Agent A parses Document 1, Agent B parses Document 2, and Supervisor Agent C reconciles conflicts
- **🧠 Deep Cross-Document Reasoning**: Uses `llama-3.3-70b-versatile` via Groq LPU for maximum inference speed
- **📊 Live Thought Trace**: Real-time visualization of agent reasoning for complete observability
- **⚠️ Conflict Detection**: Automatically identifies discrepancies between press releases, clinical trials, and FDA submissions
- **✅ Ground Truth Profile**: Produces unified asset profiles with confidence scores and conflict summaries
- **🎨 Beautiful UI**: Modern Streamlit interface with custom CSS and two-column layout

---

## 🏗️ System Architecture

```
User Input (Two Conflicting Documents)
    ↓
┌─────────────────────────────────────────┐
│  Agent A          Agent B                │
│  (Doc 1)          (Doc 2)                │
│  Extraction       Extraction             │
└─────────────┬──────────┬─────────────────┘
              ↓          ↓
        ┌──────────────────────┐
        │  Supervisor Agent C   │
        │  Reconciliation       │
        └──────────┬────────────┘
                   ↓
        ┌──────────────────────┐
        │  Ground Truth Profile │
        │  + Thought Trace      │
        └───────────────────────┘
```

**Workflow:**
1. **Ingestion**: User uploads two text blocks (e.g., Press Release vs. Clinical Trial Report)
2. **Parallel Extraction**: Two simultaneous Groq calls extract scientific parameters (Drug Name, Molecule Type, Clinical Phase, Toxicity)
3. **Reconciliation**: Supervisor agent compares outputs to identify conflicts
4. **Display**: Streamlit renders the Final Asset Profile and the "Thought Trace" side-by-side

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Inference** | Groq LPU (`llama-3.3-70b-versatile`) | Ultra-fast deep reasoning |
| **Backend** | Python + Pydantic | Type-safe data validation |
| **Frontend** | Streamlit | Real-time agent visualization |
| **Multi-Agent Logic** | Custom debate pattern | Cross-document reasoning |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Groq API key ([Get one here](https://console.groq.com))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MozartofCode/Biotech-Diligence-Tool.git
   cd Biotech-Diligence-Tool
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your Groq API key
   # GROQ_API_KEY="your_actual_groq_api_key_here"
   ```

### Running the Application

**Launch the Streamlit UI:**
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 📖 Usage Guide

### Step 1: Configure API Key
- Enter your Groq API key in the sidebar (or set it in `.env`)

### Step 2: Provide Source Documents
- **Document 1**: Select document type (Press Release, Clinical Trial Report, FDA Submission, etc.)
- Paste the first source text in the text area
- **Document 2**: Select document type and paste the second source text

### Step 3: Run Analysis
- Click the **"🚀 Run Analysis"** button
- Watch the **Agent Thought Trace** update in real-time (right column)
- View the **Verified Asset Profile** (left column)

### Step 4: Review Results
- **Confidence Score**: Indicates agreement between sources (1.0 = perfect agreement)
- **Conflicts Detected**: Number of discrepancies found
- **Thought Trace**: Complete audit trail of agent reasoning
- **Asset Profile**: Reconciled ground truth with source summary

---

## 🧪 Example Use Case

**Scenario**: Press Release vs. Clinical Trial Report

**Document 1 (Press Release):**
```
BioTech Corp announces positive Phase 2 results for BTX-501, a novel small 
molecule targeting inflammatory diseases. The drug demonstrated an excellent 
safety profile with minimal adverse events reported.
```

**Document 2 (Clinical Trial Report):**
```
BTX-501 Clinical Trial Report: Phase 1 study completed with 45 patients.
Molecule type: Small molecule kinase inhibitor. Safety findings: 12% of 
patients experienced mild-to-moderate hepatotoxicity, which was monitored 
and resolved with dose adjustment.
```

**Expected Output:**
- ⚠️ **Conflict 1**: Clinical Phase discrepancy (Phase 2 vs Phase 1)
- ⚠️ **Conflict 2**: Safety findings discrepancy (minimal AEs vs hepatotoxicity)
- **Confidence Score**: ~0.65 (lowered due to conflicts)
- **Ground Truth**: BTX-501, Small molecule, reconciled phase and safety data

---

## 🧪 Testing

### Backend Tests
```bash
python test_backend.py
```

**Tests include:**
- ✅ API Connectivity
- ✅ Pydantic Schema Integrity
- ✅ Conflict Detection
- ✅ Latency Check (Groq LPU speed)
- ✅ JSON Robustness

### Frontend Tests
```bash
python test_frontend.py
```

**Tests include:**
- ✅ File Structure
- ✅ Import Validation
- ✅ Syntax Validation
- ✅ Backend Integration
- ✅ UI Component Configuration

---

## 📁 Project Structure

```
Biotech-Diligence-Tool/
├── app.py                      # Streamlit UI with beautiful design
├── backend.py                  # Multi-agent logic with Groq API
├── requirements.txt            # Python dependencies
├── test_backend.py             # Backend test suite
├── test_frontend.py            # Frontend test suite
├── .env.example                # Environment variable template
├── .gitignore                  # Git ignore rules
├── Master_Implementation_Plan.md    # Project vision
├── design_implementation.md    # UI design specifications
└── backend_implementation.md   # Backend logic specifications
```

---

## 🎨 UI Design Philosophy

The Streamlit interface follows modern web design principles:

- **Dark Mode**: Sleek gradient background (`#0f172a` → `#1e293b`)
- **Glassmorphism**: Translucent cards with backdrop blur
- **Color-Coded Agents**: 
  - 🔵 Agent A (Blue)
  - 🟣 Agent B (Purple)
  - 🟢 Supervisor (Green)
  - 🟡 System (Amber)
- **Two-Column Layout**: 60% Asset Profile, 40% Thought Trace
- **Responsive Metrics**: Live confidence score, conflict count, analysis time

---

## 🔒 Security

- **API Key Protection**: `.env` file is excluded from version control via `.gitignore`
- **No Data Persistence**: All analysis happens in-session; no user data is stored
- **Secure Dependencies**: Regular updates to Groq, Streamlit, and Pydantic

---

## 🚧 Future Roadmap

- [ ] **Multi-Document Support**: Analyze 3+ conflicting sources simultaneously
- [ ] **PDF Ingestion**: Direct upload of scientific PDFs with text extraction
- [ ] **Export Functionality**: Download asset profiles as JSON, CSV, or PDF reports
- [ ] **Historical Tracking**: Compare how drug data changes over time
- [ ] **Custom Agent Personas**: Specialized agents for different document types
- [ ] **API Mode**: REST API for programmatic access
- [ ] **Database Integration**: Optional persistence for longitudinal studies

---

## 🤝 Contributing

Contributions are welcome! This project showcases high-agency agentic systems for Convexia (YC S25).

**Areas for improvement:**
- Enhanced conflict resolution strategies
- Additional document type support
- Improved UI/UX
- Performance optimizations

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- **Groq** for providing ultra-fast LPU inference
- **Streamlit** for the beautiful UI framework
- **Convexia (YC S25)** for the opportunity to demonstrate high-agency AI systems

---

## 📞 Contact

**Built by**: [Your Name]
**GitHub**: [MozartofCode](https://github.com/MozartofCode)
**For**: Convexia Diligence Demonstration

---

## 🎯 Core Value Proposition

**Traditional Diligence:**
- ❌ Manually read 10+ documents
- ❌ Hours of cross-referencing
- ❌ No audit trail
- ❌ Human bias

**Diligence-Zero:**
- ✅ Automated multi-source analysis
- ✅ Seconds to complete
- ✅ Full reasoning trace
- ✅ Objective conflict detection

---

**Built with 🧬 for the future of biotech diligence**
