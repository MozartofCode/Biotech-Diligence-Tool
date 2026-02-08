# Design Implementation: Streamlit "Live-Stream Trace"

## UI Layout Strategy
The goal is to show Convexia that you value **observability** (one of their key job requirements).

### 1. Layout Configuration
* **Sidebar:** API Key configuration (Groq) and "Source Data" inputs.
* **Main Stage (Columns):**
    * **Left Column (60%):** "Verified Asset Profile" – The final, clean JSON/Table output.
    * **Right Column (40%):** "Agent Thought Trace" – A scrolling log of the LLM's internal reasoning.

### 2. Components
* `st.file_uploader` or `st.text_area`: For the two conflicting scientific documents.
* `st.status` (or `st.expander`): To show the "thinking" steps in real-time.
* `st.dataframe`: To display the final scientific parameters (Binding affinity, Toxicity %%, etc).

### 3. Visual "Aha!" Moment
When a conflict is found (e.g., Doc A says Phase 2, Doc B says Phase 1), the "Agent Trace" should log: 
> `⚠️ CONFLICT DETECTED: Discrepancy in Clinical Phase. Re-evaluating based on source date...`