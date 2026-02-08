"""
Groq-Powered Multi-Agent Backend Logic
Implements the debate pattern with Agent A, Agent B, and Supervisor Agent C
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from groq import Groq
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class ScientificAsset(BaseModel):
    """Ground Truth structure for scientific asset profile"""
    drug_name: str = Field(description="Name of the drug or therapeutic asset")
    molecule_type: str = Field(description="Type of molecule (small molecule, antibody, etc.)")
    clinical_phase: str = Field(description="Current clinical development phase")
    primary_toxicity_finding: str = Field(description="Main toxicity findings from studies")
    confidence_score: float = Field(description="Confidence score 0-1 for the accuracy of data", ge=0.0, le=1.0)
    conflicts_found: List[str] = Field(default_factory=list, description="List of conflicts detected between sources")
    source_summary: Optional[str] = Field(default=None, description="Summary of data sources used")


class AgentResponse(BaseModel):
    """Structure for individual agent extraction"""
    drug_name: Optional[str] = None
    molecule_type: Optional[str] = None
    clinical_phase: Optional[str] = None
    primary_toxicity_finding: Optional[str] = None
    reasoning: str = Field(description="Agent's reasoning process")
    source_type: str = Field(description="Type of source document analyzed")


class DiligenceEngine:
    """
    Multi-Agent Diligence System using Groq LLM
    Implements debate pattern for cross-document reasoning
    """
    
    def __init__(self, api_key: str = None):
        """Initialize Groq client with API key"""
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found. Please set it in .env file")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"
        self.thought_trace = []
    
    def log_thought(self, agent: str, message: str):
        """Add entry to thought trace for observability"""
        entry = f"[{agent}] {message}"
        self.thought_trace.append(entry)
        return entry
    
    def extract_from_document(self, document_text: str, source_type: str, agent_name: str) -> AgentResponse:
        """
        Agent A or B: Extract scientific parameters from a single document
        
        Args:
            document_text: Raw text from the source document
            source_type: Type of document (e.g., "Press Release", "FDA Report")
            agent_name: Name of the agent for logging
        
        Returns:
            AgentResponse with extracted data and reasoning
        """
        self.log_thought(agent_name, f"Starting extraction from {source_type}...")
        
        prompt = f"""You are a scientific diligence analyst reviewing a {source_type}.

Extract the following information from this document:
1. Drug/Asset Name
2. Molecule Type (small molecule, antibody, peptide, etc.)
3. Clinical Development Phase (Preclinical, Phase 1, Phase 2, Phase 3, Approved)
4. Primary Toxicity Finding (any safety concerns or adverse events mentioned)

Document Text:
{document_text}

Provide your analysis in JSON format with these fields:
- drug_name
- molecule_type
- clinical_phase
- primary_toxicity_finding
- reasoning (explain your extraction process and any uncertainties)

Be precise and only extract information explicitly stated. If something is unclear or missing, state that in your reasoning.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a scientific data extraction expert. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,  # Lower temperature for more consistent extraction
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse JSON response
            # Handle markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:].strip()
            
            data = json.loads(content)
            
            agent_response = AgentResponse(
                drug_name=data.get("drug_name"),
                molecule_type=data.get("molecule_type"),
                clinical_phase=data.get("clinical_phase"),
                primary_toxicity_finding=data.get("primary_toxicity_finding"),
                reasoning=data.get("reasoning", "No reasoning provided"),
                source_type=source_type
            )
            
            self.log_thought(agent_name, f"✓ Extraction complete. Found drug: {agent_response.drug_name}")
            self.log_thought(agent_name, f"Reasoning: {agent_response.reasoning[:100]}...")
            
            return agent_response
            
        except Exception as e:
            error_msg = f"Error during extraction: {str(e)}"
            self.log_thought(agent_name, f"✗ {error_msg}")
            raise RuntimeError(error_msg)
    
    def reconcile_sources(self, agent_a_response: AgentResponse, agent_b_response: AgentResponse) -> ScientificAsset:
        """
        Supervisor Agent C: Reconcile conflicts between two document extractions
        
        Args:
            agent_a_response: Extraction from first document
            agent_b_response: Extraction from second document
        
        Returns:
            ScientificAsset with unified ground truth and conflicts
        """
        self.log_thought("Supervisor", "Starting reconciliation of sources...")
        
        prompt = f"""You are a scientific supervisor reconciling data from two different sources.

SOURCE 1 ({agent_a_response.source_type}):
- Drug Name: {agent_a_response.drug_name}
- Molecule Type: {agent_a_response.molecule_type}
- Clinical Phase: {agent_a_response.clinical_phase}
- Toxicity: {agent_a_response.primary_toxicity_finding}
- Reasoning: {agent_a_response.reasoning}

SOURCE 2 ({agent_b_response.source_type}):
- Drug Name: {agent_b_response.drug_name}
- Molecule Type: {agent_b_response.molecule_type}
- Clinical Phase: {agent_b_response.clinical_phase}
- Toxicity: {agent_b_response.primary_toxicity_finding}
- Reasoning: {agent_b_response.reasoning}

Your task:
1. Identify any CONFLICTS between the two sources
2. Determine the most reliable "ground truth" for each parameter
3. Assign a confidence score (0.0 to 1.0) based on agreement between sources
4. List all conflicts found

Respond in JSON format with these fields:
- drug_name (reconciled name)
- molecule_type (reconciled type)
- clinical_phase (reconciled phase)
- primary_toxicity_finding (reconciled finding)
- confidence_score (0.0 to 1.0, higher when sources agree)
- conflicts_found (list of strings describing each conflict)
- source_summary (brief summary of how you reconciled the data)

If sources perfectly agree, confidence_score should be 1.0 and conflicts_found should be empty.
If there are major discrepancies, confidence_score should be lower and conflicts should be detailed.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a scientific reconciliation expert. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse JSON response
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:].strip()
            
            data = json.loads(content)
            
            # Log conflicts if found
            if data.get("conflicts_found"):
                for conflict in data["conflicts_found"]:
                    self.log_thought("Supervisor", f"⚠️ CONFLICT DETECTED: {conflict}")
            else:
                self.log_thought("Supervisor", "✓ Sources are in agreement")
            
            asset = ScientificAsset(
                drug_name=data["drug_name"],
                molecule_type=data["molecule_type"],
                clinical_phase=data["clinical_phase"],
                primary_toxicity_finding=data["primary_toxicity_finding"],
                confidence_score=data["confidence_score"],
                conflicts_found=data.get("conflicts_found", []),
                source_summary=data.get("source_summary")
            )
            
            self.log_thought("Supervisor", f"✓ Reconciliation complete. Confidence: {asset.confidence_score:.2%}")
            
            return asset
            
        except Exception as e:
            error_msg = f"Error during reconciliation: {str(e)}"
            self.log_thought("Supervisor", f"✗ {error_msg}")
            raise RuntimeError(error_msg)
    
    def process_dual_documents(self, doc1_text: str, doc1_type: str, doc2_text: str, doc2_type: str) -> tuple[ScientificAsset, List[str]]:
        """
        Main workflow: Process two documents and return reconciled asset profile
        
        Args:
            doc1_text: Text content of first document
            doc1_type: Type of first document (e.g., "Press Release")
            doc2_text: Text content of second document
            doc2_type: Type of second document (e.g., "Clinical Trial Report")
        
        Returns:
            Tuple of (ScientificAsset, thought_trace)
        """
        # Reset thought trace for new analysis
        self.thought_trace = []
        
        self.log_thought("System", f"🚀 Starting dual-document analysis: {doc1_type} vs {doc2_type}")
        
        # Parallel extraction (Agent A and Agent B)
        agent_a_response = self.extract_from_document(doc1_text, doc1_type, "Agent A")
        agent_b_response = self.extract_from_document(doc2_text, doc2_type, "Agent B")
        
        # Reconciliation (Supervisor Agent C)
        final_asset = self.reconcile_sources(agent_a_response, agent_b_response)
        
        self.log_thought("System", "✅ Analysis complete. Asset profile ready.")
        
        return final_asset, self.thought_trace.copy()


# Example usage and testing
if __name__ == "__main__":
    # Test the backend with sample data
    engine = DiligenceEngine()
    
    # Sample conflicting documents
    press_release = """
    BioTech Corp announces positive Phase 2 results for BTX-501, a novel small molecule
    targeting inflammatory diseases. The drug demonstrated excellent safety profile with
    minimal adverse events reported.
    """
    
    clinical_report = """
    BTX-501 Clinical Trial Report: Phase 1 study completed with 45 patients.
    Molecule type: Small molecule inhibitor. Safety findings: 12% of patients experienced
    mild hepatotoxicity, monitored and resolved with dose adjustment.
    """
    
    try:
        asset, trace = engine.process_dual_documents(
            press_release, "Press Release",
            clinical_report, "Clinical Trial Report"
        )
        
        print("\n=== FINAL ASSET PROFILE ===")
        print(asset.model_dump_json(indent=2))
        
        print("\n\n=== THOUGHT TRACE ===")
        for thought in trace:
            print(thought)
            
    except Exception as e:
        print(f"Error: {e}")
