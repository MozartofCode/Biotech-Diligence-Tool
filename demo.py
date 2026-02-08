"""
Quick Demo of Diligence-Zero Backend
Runs a sample analysis to demonstrate the system capabilities
"""

from backend import DiligenceEngine
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()

def run_demo():
    print("\n" + "🧬" * 40)
    print("  DILIGENCE-ZERO DEMO")
    print("  Multi-Agent Biotech Asset Analysis")
    print("🧬" * 40 + "\n")
    
    # Check API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ ERROR: GROQ_API_KEY not found in .env file")
        print("   Please create a .env file with your Groq API key")
        return
    
    print("✅ API Key found")
    print("🚀 Initializing Diligence Engine...\n")
    
    # Initialize engine
    engine = DiligenceEngine(api_key=api_key)
    
    # Sample conflicting documents
    press_release = """
    SynapTech Pharmaceuticals announces breakthrough Phase 2 results for SYN-400,
    a novel monoclonal antibody targeting neurodegenerative diseases. The Phase 2
    trial enrolled 250 patients with Alzheimer's disease and demonstrated significant
    cognitive improvements. The drug showed an excellent safety profile with no
    serious adverse events reported. SYN-400 is on track for Phase 3 trials in Q4 2026.
    """
    
    clinical_report = """
    Clinical Trial Update - SYN-400 Safety Assessment
    
    Trial Phase: Phase 1 dose-escalation study (completed December 2025)
    Molecule: Humanized monoclonal antibody targeting beta-amyloid
    Patient Population: 80 healthy volunteers and 45 early-stage Alzheimer's patients
    
    Safety Findings:
    - 18% of patients in high-dose cohort experienced infusion-related reactions
    - Moderate transient thrombocytopenia observed in 8% of patients
    - All events resolved within 72 hours with dose modification
    - Study concluding Phase 1; Phase 2 planning underway
    
    Recommendation: Proceed to Phase 2 with modified dosing protocol
    """
    
    print("=" * 80)
    print("DOCUMENT 1: PRESS RELEASE")
    print("=" * 80)
    print(press_release.strip())
    
    print("\n" + "=" * 80)
    print("DOCUMENT 2: CLINICAL TRIAL REPORT")
    print("=" * 80)
    print(clinical_report.strip())
    
    print("\n" + "=" * 80)
    print("INITIATING MULTI-AGENT ANALYSIS")
    print("=" * 80 + "\n")
    
    # Run analysis
    try:
        asset, trace = engine.process_dual_documents(
            press_release, "Press Release",
            clinical_report, "Clinical Trial Report"
        )
        
        print("\n" + "🧠" * 40)
        print("  AGENT THOUGHT TRACE")
        print("🧠" * 40 + "\n")
        
        for thought in trace:
            # Color code the output
            if "[Agent A]" in thought:
                print(f"\033[94m{thought}\033[0m")  # Blue
            elif "[Agent B]" in thought:
                print(f"\033[95m{thought}\033[0m")  # Magenta
            elif "[Supervisor]" in thought:
                print(f"\033[92m{thought}\033[0m")  # Green
            elif "[System]" in thought:
                print(f"\033[93m{thought}\033[0m")  # Yellow
            else:
                print(thought)
        
        print("\n" + "📊" * 40)
        print("  VERIFIED ASSET PROFILE (GROUND TRUTH)")
        print("📊" * 40 + "\n")
        
        print(f"Drug Name:              {asset.drug_name}")
        print(f"Molecule Type:          {asset.molecule_type}")
        print(f"Clinical Phase:         {asset.clinical_phase}")
        print(f"Confidence Score:       {asset.confidence_score:.1%}")
        print(f"\nPrimary Toxicity Finding:")
        print(f"  {asset.primary_toxicity_finding}")
        
        if asset.conflicts_found:
            print(f"\n⚠️  CONFLICTS DETECTED ({len(asset.conflicts_found)}):")
            for i, conflict in enumerate(asset.conflicts_found, 1):
                print(f"  {i}. {conflict}")
        else:
            print(f"\n✅ No conflicts detected - sources in perfect agreement!")
        
        if asset.source_summary:
            print(f"\n📝 Reconciliation Summary:")
            print(f"  {asset.source_summary}")
        
        print("\n" + "=" * 80)
        print("✅ DEMO COMPLETE")
        print("=" * 80)
        
        print("\n💡 Key Insights:")
        print(f"   • Detected {len(asset.conflicts_found)} conflict(s) between sources")
        print(f"   • Confidence score: {asset.confidence_score:.0%} (lower = more conflicts)")
        print(f"   • Multi-agent system successfully reconciled conflicting data")
        print(f"   • Complete audit trail available in thought trace")
        
        print("\n🚀 Next Steps:")
        print("   • Run: streamlit run app.py")
        print("   • Open http://localhost:8501 in your browser")
        print("   • Experience the beautiful UI with real-time thought trace!")
        
    except Exception as e:
        print(f"\n❌ ERROR during analysis: {str(e)}")
        print("   Please check your Groq API key and internet connection")

if __name__ == "__main__":
    run_demo()
