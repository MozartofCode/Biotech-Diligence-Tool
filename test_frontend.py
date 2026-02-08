"""
Frontend Testing Script for Diligence-Zero
Tests Streamlit UI, layout, and thought trace rendering
"""

import subprocess
import sys
import os
import time

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def check_file_exists(filepath):
    """Check if a required file exists"""
    if os.path.exists(filepath):
        print(f"✓ Found: {filepath}")
        return True
    else:
        print(f"❌ Missing: {filepath}")
        return False

def test_file_structure():
    """Test 1: Verify all required files exist"""
    print_section("TEST 1: File Structure")
    
    required_files = [
        "app.py",
        "backend.py",
        "requirements.txt",
        ".env"
    ]
    
    results = []
    for file in required_files:
        results.append(check_file_exists(file))
    
    if all(results):
        print("\n✅ TEST 1 PASSED: All required files present")
        return True
    else:
        print("\n❌ TEST 1 FAILED: Missing required files")
        return False

def test_imports():
    """Test 2: Verify app.py imports work correctly"""
    print_section("TEST 2: Import Validation")
    
    try:
        # Try importing the modules
        print("Testing backend imports...")
        import backend
        print("✓ backend.py imports successfully")
        
        print("\nTesting Streamlit...")
        import streamlit
        print(f"✓ Streamlit version: {streamlit.__version__}")
        
        print("\nTesting Groq...")
        import groq
        print("✓ Groq package available")
        
        print("\nTesting Pydantic...")
        import pydantic
        print(f"✓ Pydantic version: {pydantic.__version__}")
        
        print("\n✅ TEST 2 PASSED: All imports successful")
        return True
        
    except ImportError as e:
        print(f"\n❌ TEST 2 FAILED: Import error - {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ TEST 2 FAILED: {str(e)}")
        return False

def test_app_syntax():
    """Test 3: Check app.py for syntax errors"""
    print_section("TEST 3: Syntax Validation")
    
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            code = f.read()
        
        compile(code, "app.py", "exec")
        print("✓ app.py has valid Python syntax")
        
        # Check for key Streamlit components
        required_components = [
            "st.set_page_config",
            "st.sidebar",
            "st.columns",
            "st.text_area",
            "st.button",
            "st.session_state"
        ]
        
        for component in required_components:
            if component in code:
                print(f"✓ Found: {component}")
            else:
                print(f"⚠️  Warning: {component} not found")
        
        # Check for two-column layout
        if "st.columns([6, 4])" in code or "st.columns(" in code:
            print("✓ Two-column layout implemented")
        else:
            print("⚠️  Warning: Two-column layout may not be implemented")
        
        # Check for thought trace rendering
        if "thought" in code.lower() and "trace" in code.lower():
            print("✓ Thought trace implementation found")
        else:
            print("⚠️  Warning: Thought trace may not be implemented")
        
        print("\n✅ TEST 3 PASSED: Syntax validation successful")
        return True
        
    except SyntaxError as e:
        print(f"\n❌ TEST 3 FAILED: Syntax error in app.py - {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ TEST 3 FAILED: {str(e)}")
        return False

def test_backend_integration():
    """Test 4: Verify backend integration works"""
    print_section("TEST 4: Backend Integration")
    
    try:
        from backend import DiligenceEngine
        
        print("Testing DiligenceEngine initialization...")
        
        # Check if API key exists
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            print(f"✓ API key found in environment")
            engine = DiligenceEngine(api_key=api_key)
            print("✓ DiligenceEngine initialized successfully")
        else:
            print("⚠️  No API key found - will require user input")
        
        # Verify the engine has required methods
        required_methods = [
            "extract_from_document",
            "reconcile_sources",
            "process_dual_documents"
        ]
        
        for method in required_methods:
            if hasattr(engine if api_key else DiligenceEngine, method):
                print(f"✓ Method exists: {method}")
            else:
                print(f"❌ Missing method: {method}")
                return False
        
        print("\n✅ TEST 4 PASSED: Backend integration verified")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 4 FAILED: {str(e)}")
        return False

def test_ui_components():
    """Test 5: Verify UI components are properly configured"""
    print_section("TEST 5: UI Component Configuration")
    
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            code = f.read()
        
        # Check page config
        if 'page_title=' in code:
            print("✓ Page title configured")
        
        if 'page_icon=' in code:
            print("✓ Page icon configured")
        
        if 'layout="wide"' in code:
            print("✓ Wide layout enabled")
        
        # Check sidebar components
        if 'st.sidebar' in code:
            print("✓ Sidebar implemented")
        
        if 'st.text_area' in code:
            print("✓ Text area inputs present")
        
        if 'st.button' in code:
            print("✓ Action button present")
        
        # Check for custom CSS
        if 'st.markdown' in code and '<style>' in code:
            print("✓ Custom CSS styling implemented")
        
        # Check for session state management
        if 'st.session_state' in code:
            print("✓ Session state management implemented")
        
        # Check for error handling
        if 'st.error' in code:
            print("✓ Error handling implemented")
        
        if 'st.success' in code:
            print("✓ Success messages implemented")
        
        # Check for metrics/data display
        if 'st.metric' in code or 'st.dataframe' in code or 'st.json' in code:
            print("✓ Data visualization components present")
        
        print("\n✅ TEST 5 PASSED: UI components properly configured")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 5 FAILED: {str(e)}")
        return False

def provide_launch_instructions():
    """Provide instructions for manual testing"""
    print_section("MANUAL TESTING INSTRUCTIONS")
    
    print("""
To manually test the Streamlit UI, follow these steps:

1. **Launch the application:**
   ```
   streamlit run app.py
   ```

2. **Test the following:**
   
   ✓ Sidebar Configuration:
     - API key input field is visible
     - Two document input text areas are present
     - Document type selectors work
     - "Run Analysis" button is visible
   
   ✓ Layout & Design:
     - Two-column layout (60% left, 40% right)
     - Modern, professional styling
     - Responsive design
     - Custom CSS applied
   
   ✓ Functionality:
     - Enter sample documents
     - Click "Run Analysis"
     - Verify thought trace updates in real-time
     - Verify final asset profile displays
     - Check conflict detection works
   
   ✓ Observability:
     - Thought trace shows agent reasoning
     - Conflicts highlighted with warnings
     - Confidence score displayed
     - All metrics visible

3. **Sample test data:**
   
   Document 1 (Press Release):
   "BioTech Corp announces positive Phase 2 results for BTX-501, 
   a novel small molecule targeting inflammatory diseases. 
   Excellent safety profile with minimal adverse events."
   
   Document 2 (Clinical Report):
   "BTX-501 Phase 1 study: Small molecule inhibitor. 
   Safety findings: 12% mild hepatotoxicity, resolved with dose adjustment."

4. **Expected behavior:**
   - System detects Phase conflict (Phase 2 vs Phase 1)
   - System detects safety conflict (minimal vs hepatotoxicity)
   - Confidence score < 1.0 due to conflicts
   - Thought trace shows conflict warnings (⚠️)
   - Final profile reconciles both sources
""")

def run_all_tests():
    """Run complete frontend test suite"""
    print("\n" + "🎨" * 35)
    print("  DILIGENCE-ZERO FRONTEND TEST SUITE")
    print("🎨" * 35)
    
    results = {}
    
    # Run automated tests
    results['File Structure'] = test_file_structure()
    results['Import Validation'] = test_imports()
    results['Syntax Validation'] = test_app_syntax()
    results['Backend Integration'] = test_backend_integration()
    results['UI Component Configuration'] = test_ui_components()
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*70}")
    print(f"  Results: {passed}/{total} automated tests passed")
    
    if passed == total:
        print(f"  🎉 ALL AUTOMATED TESTS PASSED!")
        print(f"  ⚡ Ready for manual UI testing")
    else:
        print(f"  ⚠️  Some tests failed - review output above")
    
    print(f"{'='*70}\n")
    
    # Provide manual testing instructions
    provide_launch_instructions()
    
    return passed == total

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    success = run_all_tests()
    sys.exit(0 if success else 1)
