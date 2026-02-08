---
name: test-frontend
description: Handles the development and testing of the Streamlit UI. Use this to build layouts and verify that the "Thought Trace" renders in real-time.
---

# Frontend Build & Test Skill

## Development Instructions
1. **Layout**: Implement a two-column layout (`st.columns`) as per the "Live-Stream Trace" design.
2. **State Management**: Use `st.session_state` to maintain the "Thought Trace" history as the agent streams data.
3. **Streaming**: Ensure `st.write_stream` or an equivalent loop is used for the Groq output to create the "real-time" effect.

## Testing Checklist
1. **Rendering**: Run `streamlit run app.py` and verify the UI loads without errors.
2. **Input Handling**: Test the `st.text_area` or `st.file_uploader` with large scientific texts.
3. **Observability**: Verify that the "Thought Trace" panel updates *before* the final JSON profile is displayed.
4. **Responsive Check**: Ensure the sidebar configuration does not overlap with the main content.