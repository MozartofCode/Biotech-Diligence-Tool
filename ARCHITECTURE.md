# Diligence-Zero System Architecture

```
                    🧬 DILIGENCE-ZERO ARCHITECTURE 🧬
                    Multi-Agent Biotech Asset Analysis
                    
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INPUTS                                  │
└─────────────────────────────────────────────────────────────────────┘
                            │          │
         ┌──────────────────┘          └──────────────────┐
         │                                                 │
         ▼                                                 ▼
┌──────────────────────┐                      ┌──────────────────────┐
│  📄 Document 1       │                      │  📄 Document 2       │
│  (Press Release)     │                      │  (Clinical Report)   │
│                      │                      │                      │
│  • Drug name         │                      │  • Trial data        │
│  • Claims            │                      │  • Safety findings   │
│  • Marketing info    │                      │  • Actual results    │
└──────────┬───────────┘                      └──────────┬───────────┘
           │                                             │
           │ Groq API Call                Groq API Call │
           │ (Extract)                        (Extract) │
           │                                             │
           ▼                                             ▼
┌──────────────────────┐                      ┌──────────────────────┐
│  🤖 AGENT A          │                      │  🤖 AGENT B          │
│  (Document Parser)   │                      │  (Document Parser)   │
│                      │                      │                      │
│  Extracts:           │                      │  Extracts:           │
│  • Drug name         │                      │  • Drug name         │
│  • Molecule type     │                      │  • Molecule type     │
│  • Clinical phase    │                      │  • Clinical phase    │
│  • Toxicity data     │                      │  • Toxicity data     │
│                      │                      │                      │
│  + Reasoning trace   │                      │  + Reasoning trace   │
└──────────┬───────────┘                      └──────────┬───────────┘
           │                                             │
           │         AgentResponse (Pydantic)            │
           └─────────────────┬──────────────────────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  🧠 SUPERVISOR       │
                  │  AGENT C             │
                  │  (Reconciliation)    │
                  │                      │
                  │  Compares outputs:   │
                  │  ✓ Find conflicts    │
                  │  ✓ Reconcile data    │
                  │  ✓ Assign confidence │
                  │  ✓ Generate summary  │
                  │                      │
                  │  Groq API Call       │
                  │  (Synthesize)        │
                  └──────────┬───────────┘
                             │
                             │ ScientificAsset (Pydantic)
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        OUTPUTS                                       │
├─────────────────────────────────┬───────────────────────────────────┤
│  📊 GROUND TRUTH PROFILE        │  🧠 THOUGHT TRACE                 │
│                                 │                                   │
│  ✓ Drug Name                    │  [System] Analysis started        │
│  ✓ Molecule Type                │  [Agent A] Extracting Doc 1...    │
│  ✓ Clinical Phase (reconciled)  │  [Agent A] Found: BTX-501         │
│  ✓ Primary Toxicity             │  [Agent B] Extracting Doc 2...    │
│  ✓ Confidence Score: 0.0-1.0    │  [Agent B] Found: BTX-501         │
│  ✓ Conflicts Found: [...list]  │  [Supervisor] Reconciling...      │
│  ✓ Source Summary               │  [Supervisor] ⚠️ CONFLICT: Phase  │
│                                 │  [Supervisor] ⚠️ CONFLICT: Safety │
│  Display in Streamlit UI        │  [System] Analysis complete       │
│  (Left column, 60%)             │  (Right column, 40%)              │
└─────────────────────────────────┴───────────────────────────────────┘
                             │
                             ▼
                    USER REVIEWS RESULTS
                    with complete audit trail

═══════════════════════════════════════════════════════════════════════

                        TECHNOLOGY STACK

┌─────────────────────────────────────────────────────────────────────┐
│  Inference Engine:   Groq LPU (llama-3.3-70b-versatile)            │
│  Backend Logic:      Python 3.9+ with Pydantic for type safety     │
│  Frontend UI:        Streamlit with custom CSS                     │
│  Multi-Agent:        Custom debate pattern implementation          │
│  Observability:      Real-time thought trace logging               │
└─────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════

                        KEY CAPABILITIES

✅  Conflict Detection       Identifies discrepancies between sources
✅  Cross-Document Reasoning Uses context from both documents
✅  Confidence Scoring       Lower score when conflicts detected  
✅  Complete Audit Trail     Every decision is logged and traceable
✅  Real-Time Visualization  Live updates in Streamlit UI
✅  Type-Safe Validation     Pydantic ensures data integrity
✅  Ultra-Fast Inference     ~1.88s average (Groq LPU)

═══════════════════════════════════════════════════════════════════════

                        WORKFLOW SUMMARY

1️⃣  USER inputs two conflicting scientific documents
2️⃣  Agent A & Agent B extract data in parallel (Groq API)
3️⃣  Both agents log their reasoning to thought trace
4️⃣  Supervisor Agent C receives both extractions
5️⃣  Supervisor identifies conflicts and reconciles data
6️⃣  Supervisor logs conflict warnings to thought trace
7️⃣  Final asset profile created with confidence score
8️⃣  Streamlit displays profile + trace side-by-side
9️⃣  USER reviews results with complete transparency

═══════════════════════════════════════════════════════════════════════

Built for Convexia (YC S25) | Powered by Groq LPU | MIT License
```
