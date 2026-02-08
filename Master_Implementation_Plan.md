# Master Implementation Plan: Diligence-Zero

## 1. Ultimate Goal
To demonstrate a "High-Agency" agentic system that can ingest conflicting scientific drug data from multiple sources, perform cross-document reasoning, and produce a unified "Ground Truth" asset profile with a clear audit trail.

## 2. Audience & Business Requirements
* **Target:** Founders at Convexia (YC S25).
* **Value Prop:** Reduces manual asset diligence from hours to seconds by identifying "Confidence Gaps" between public press releases and clinical trial data.
* **Key Requirement:** The system must not just provide an answer, but show the "Reasoning Trace" to ensure reliability.

## 3. Tech Requirements
* **Inference:** Groq LPU (using `llama-3.3-70b-versatile` for deep reasoning).
* **Logic:** Multi-agent "Debate" pattern (Agent A parses Doc 1, Agent B parses Doc 2, Agent C reconciles).
* **Frontend:** Streamlit (for real-time visualization of agent thoughts).
* **Data Handling:** Python-based text normalization.

## 4. System Architecture
1.  **Ingestion:** User uploads two text blocks (e.g., Press Release vs. FDA Data).
2.  **Extraction:** Two parallel Groq calls extract specific scientific parameters (Toxicity, Phase, Molecule Type).
3.  **Reconciliation:** A "Supervisor" call compares both outputs to find discrepancies.
4.  **Display:** Streamlit renders the Final Asset Profile and the "Thought Trace" side-by-side.

---
*Refer to `Design_implementation.md` for UI layout and `Backend_implementation.md` for Groq logic.*