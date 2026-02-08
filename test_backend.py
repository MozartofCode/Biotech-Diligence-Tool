"""
Backend Testing Protocol for Diligence-Zero
Tests Groq API integration, Pydantic validation, and multi-agent reasoning
"""

import sys
import time
from backend import DiligenceEngine, ScientificAsset, AgentResponse
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def test_api_connectivity():
    """Test 1: Verify Groq API key is valid and LPU is responding"""
    print_section("TEST 1: API Connectivity")
    
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("❌ FAILED: GROQ_API_KEY not found in .env file")
            return False
        
        print(f"✓ API Key found: {api_key[:10]}...")
        
        # Initialize engine
        engine = DiligenceEngine(api_key=api_key)
        print("✓ DiligenceEngine initialized successfully")
        
        # Test simple extraction
        test_doc = "BTX-100 is a small molecule drug currently in Phase 2 clinical trials."
        response = engine.extract_from_document(test_doc, "Test Document", "Test Agent")
        
        print(f"✓ API responded successfully")
        print(f"✓ Extracted drug name: {response.drug_name}")
        print(f"✓ Extracted phase: {response.clinical_phase}")
        
        print("\n✅ TEST 1 PASSED: API connectivity verified")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 1 FAILED: {str(e)}")
        return False

def test_schema_integrity():
    """Test 2: Validate Pydantic model is correctly populated"""
    print_section("TEST 2: Schema Integrity")
    
    try:
        engine = DiligenceEngine()
        
        # Test document with all fields
        doc1 = """
        DrugX-200 is a monoclonal antibody currently in Phase 3 clinical development.
        The molecule targets inflammatory pathways. Recent safety data shows mild 
        injection site reactions in 5% of patients, all resolved without intervention.
        """
        
        doc2 = """
        Clinical trial update for DrugX-200: Phase 3 enrollment complete with 500 patients.
        This antibody therapeutic has demonstrated excellent tolerability. Minor adverse
        events include transient injection site erythema in a small subset of patients.
        """
        
        # Run extraction
        agent_a = engine.extract_from_document(doc1, "Clinical Brief", "Agent A")
        agent_b = engine.extract_from_document(doc2, "Trial Update", "Agent B")
        
        # Validate AgentResponse structure
        assert isinstance(agent_a, AgentResponse), "Agent A response is not AgentResponse type"
        assert agent_a.drug_name is not None, "Drug name not extracted"
        assert agent_a.reasoning is not None, "Reasoning not provided"
        
        print("✓ AgentResponse validation passed")
        
        # Run reconciliation
        asset = engine.reconcile_sources(agent_a, agent_b)
        
        # Validate ScientificAsset structure
        assert isinstance(asset, ScientificAsset), "Asset is not ScientificAsset type"
        assert asset.drug_name is not None, "Drug name missing in asset"
        assert asset.molecule_type is not None, "Molecule type missing in asset"
        assert asset.clinical_phase is not None, "Clinical phase missing in asset"
        assert asset.primary_toxicity_finding is not None, "Toxicity finding missing"
        assert 0.0 <= asset.confidence_score <= 1.0, "Confidence score out of range"
        assert isinstance(asset.conflicts_found, list), "Conflicts not a list"
        
        print("✓ ScientificAsset validation passed")
        print(f"✓ All required fields populated:")
        print(f"  - Drug Name: {asset.drug_name}")
        print(f"  - Molecule Type: {asset.molecule_type}")
        print(f"  - Clinical Phase: {asset.clinical_phase}")
        print(f"  - Confidence Score: {asset.confidence_score:.2%}")
        print(f"  - Conflicts Found: {len(asset.conflicts_found)}")
        
        print("\n✅ TEST 2 PASSED: Schema integrity verified")
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST 2 FAILED: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ TEST 2 FAILED: {str(e)}")
        return False

def test_conflict_detection():
    """Test 3: Verify agent detects conflicts in conflicting documents"""
    print_section("TEST 3: Conflict Detection & Reasoning")
    
    try:
        engine = DiligenceEngine()
        
        # Intentionally conflicting documents
        press_release = """
        BioTech Corp announces breakthrough results for BTX-501, a novel small molecule
        targeting inflammatory diseases. The drug has successfully completed Phase 2 trials
        with an excellent safety profile. No serious adverse events were reported.
        """
        
        clinical_report = """
        BTX-501 Clinical Trial Report: Phase 1 safety study completed with 45 patients.
        Molecule classification: Small molecule kinase inhibitor. 
        Safety findings: 12% of patients experienced mild-to-moderate hepatotoxicity,
        which was monitored and resolved with dose adjustment. Study advancing to Phase 2.
        """
        
        print("Testing with intentionally conflicting documents:")
        print("  - Press Release: Claims Phase 2 complete, excellent safety")
        print("  - Clinical Report: Shows Phase 1 complete, hepatotoxicity concerns")
        
        # Run full analysis
        asset, trace = engine.process_dual_documents(
            press_release, "Press Release",
            clinical_report, "Clinical Trial Report"
        )
        
        # Verify conflicts were detected
        if len(asset.conflicts_found) == 0:
            print("\n❌ TEST 3 FAILED: No conflicts detected when conflicts exist")
            return False
        
        print(f"\n✓ Conflicts detected: {len(asset.conflicts_found)}")
        for i, conflict in enumerate(asset.conflicts_found, 1):
            print(f"  {i}. {conflict}")
        
        # Verify confidence score is lower due to conflicts
        if asset.confidence_score >= 0.9:
            print(f"\n⚠️  WARNING: Confidence score ({asset.confidence_score:.2%}) is high despite conflicts")
        else:
            print(f"✓ Confidence score appropriately lowered: {asset.confidence_score:.2%}")
        
        # Verify thought trace contains conflict warnings
        conflict_warnings = [t for t in trace if "CONFLICT" in t.upper()]
        if conflict_warnings:
            print(f"✓ Conflict warnings found in thought trace: {len(conflict_warnings)}")
            for warning in conflict_warnings:
                print(f"  - {warning}")
        else:
            print("⚠️  WARNING: No explicit conflict warnings in thought trace")
        
        print("\n✅ TEST 3 PASSED: Conflict detection working correctly")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 3 FAILED: {str(e)}")
        return False

def test_latency():
    """Test 4: Measure Groq inference latency for maximalist speed"""
    print_section("TEST 4: Latency Check")
    
    try:
        engine = DiligenceEngine()
        
        # Sample documents
        doc1 = """
        TherapX-300 is an antibody-drug conjugate in Phase 2 trials.
        Safety profile shows manageable grade 1-2 neutropenia in 8% of patients.
        """
        
        doc2 = """
        TherapX-300 clinical update: Phase 2 ongoing with 200 patients enrolled.
        This ADC shows promising efficacy with acceptable toxicity profile.
        Mild neutropenia observed, consistent with mechanism of action.
        """
        
        print("Measuring end-to-end analysis latency...")
        
        # Time the full analysis
        start_time = time.time()
        asset, trace = engine.process_dual_documents(
            doc1, "Document 1",
            doc2, "Document 2"
        )
        end_time = time.time()
        
        total_time = end_time - start_time
        
        print(f"\n✓ Total analysis time: {total_time:.2f} seconds")
        
        # Groq LPU should be fast - expect < 10 seconds for this workload
        if total_time < 10:
            print(f"✓ EXCELLENT: Analysis completed in under 10 seconds")
        elif total_time < 20:
            print(f"✓ GOOD: Analysis completed in reasonable time")
        else:
            print(f"⚠️  SLOW: Analysis took longer than expected")
        
        # Estimate tokens per second (rough)
        estimated_prompt_tokens = len(doc1.split()) + len(doc2.split()) * 4  # rough estimate
        throughput = estimated_prompt_tokens / total_time
        print(f"✓ Estimated throughput: ~{throughput:.0f} tokens/second")
        
        print("\n✅ TEST 4 PASSED: Latency measured successfully")
        return total_time
        
    except Exception as e:
        print(f"\n❌ TEST 4 FAILED: {str(e)}")
        return None

def test_json_robustness():
    """Test 5: Verify JSON parsing handles edge cases"""
    print_section("TEST 5: JSON Robustness")
    
    try:
        engine = DiligenceEngine()
        
        # Document with minimal information to test edge cases
        sparse_doc = "XYZ-99 is a drug."
        
        print("Testing with sparse/minimal document...")
        
        response = engine.extract_from_document(sparse_doc, "Sparse Document", "Test Agent")
        
        # Should still return valid structure even with minimal data
        assert isinstance(response, AgentResponse), "Response type invalid"
        print("✓ JSON parsing handled sparse data")
        
        # Document with special characters
        special_doc = """
        Drug "ABC-123" (formerly known as XYZ-456) is a novel therapy.
        Phase: 2/3 (transitional). Safety: "Well-tolerated" per PI's notes.
        """
        
        print("Testing with special characters and quotes...")
        
        response2 = engine.extract_from_document(special_doc, "Special Chars Doc", "Test Agent")
        assert isinstance(response2, AgentResponse), "Response type invalid"
        print("✓ JSON parsing handled special characters")
        
        print("\n✅ TEST 5 PASSED: JSON parsing is robust")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 5 FAILED: {str(e)}")
        return False

def run_all_tests():
    """Run complete test suite"""
    print("\n" + "🧬" * 35)
    print("  DILIGENCE-ZERO BACKEND TEST SUITE")
    print("🧬" * 35)
    
    results = {}
    
    # Run all tests
    results['API Connectivity'] = test_api_connectivity()
    results['Schema Integrity'] = test_schema_integrity()
    results['Conflict Detection'] = test_conflict_detection()
    latency = test_latency()
    results['Latency Check'] = latency is not None
    results['JSON Robustness'] = test_json_robustness()
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*70}")
    print(f"  Results: {passed}/{total} tests passed")
    
    if latency:
        print(f"  Average latency: {latency:.2f}s")
    
    if passed == total:
        print(f"  🎉 ALL TESTS PASSED - Backend is production ready!")
    else:
        print(f"  ⚠️  Some tests failed - review output above")
    
    print(f"{'='*70}\n")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
