---
name: test-backend
description: Tests the backend logic, specifically Groq API integration and Pydantic data validation. Use this to ensure agents are reasoning correctly.
---

# Backend Testing Protocol

## Validation Steps
1. **API Connectivity**: Run a minimal test script to verify the Groq API key is valid and the LPU is responding.
2. **Schema Integrity**: Validate that the LLM response correctly populates the `ScientificAsset` Pydantic model.
3. **Reasoning Check**:
   - Input: Two documents with conflicting clinical phases.
   - Expected Output: The agent must flag a conflict in the `conflicts_found` list.
4. **Latency Check**: Log how long the Groq inference takes to ensure "maximalist speed."

## Failure Recovery
- If the JSON is malformed, suggest a "Retry with JSON Mode" prompt adjustment.
- If the API rate limits, implement a basic backoff strategy.