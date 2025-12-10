import streamlit as st
import sys
import os
import json
import pandas as pd

# Add current directory to path to allow importing from execution folder
sys.path.append(os.getcwd())

try:
    from execution.parse_workout import parse_workout
except ImportError:
    st.error("Could not import `execution.parse_workout`. Make sure `execution/parse_workout.py` exists.")
    st.stop()

st.set_page_config(page_title="GymLog", page_icon="💪", layout="centered")

st.title("💪 GymLog")
st.markdown("Import your workout notes from your iPhone to track your progress.")

# Sidebar for instructions
with st.sidebar:
    st.header("How to use")
    st.markdown("1. Copy your workout note from iPhone Notes.")
    st.markdown("2. Paste it into the text area.")
    st.markdown("3. Click 'Process Workout'.")
    st.markdown("---")
    st.markdown("**Note**: You can access this app on your phone by finding your computer's IP address (e.g. `192.168.1.x:8501`) if on the same Wi-Fi.")

# Main Input
workout_text = st.text_area("Paste your workout here:", height=300)

if st.button("Process Workout", type="primary"):
    if not workout_text.strip():
        st.warning("Please paste some text first!")
    else:
        with st.spinner("Parsing workout with Gemini..."):
            result_json_str = parse_workout(workout_text)
            
            try:
                # Parse the raw JSON string returned by the logic layer
                data = json.loads(result_json_str)
                
                # Check for error key
                if "error" in data:
                    st.error(f"Error parsing workout: {data['error']}")
                else:
                    st.success(f"Parsed: {data.get('routineName', 'Workout')}")
                    
                    # Display as neat cards or table
                    exercises = data.get("exercises", [])
                    
                    if exercises:
                        # Convert to DataFrame for a nice table view
                        df = pd.DataFrame(exercises)
                        
                        # Reorder columns if they exist
                        cols = ["name", "sets", "reps", "weight", "notes"]
                        clean_cols = [c for c in cols if c in df.columns]
                        st.dataframe(df[clean_cols], use_container_width=True, hide_index=True)
                        
                        # Visual cards loop
                        st.subheader("Exercise Details")
                        for ex in exercises:
                            with st.expander(f"{ex.get('name', 'Exercise')} - {ex.get('sets')} x {ex.get('reps')}"):
                                st.write(f"**Weight**: {ex.get('weight', 'N/A')}")
                                if ex.get('notes'):
                                    st.info(f"Note: {ex.get('notes')}")
                    else:
                        st.info("No exercises found in the text.")
                        
                # Show raw JSON for debugging (optional, maybe in an expander)
                with st.expander("View Raw JSON"):
                    st.json(data)
                    
            except json.JSONDecodeError:
                st.error("Failed to decode JSON response from the model.")
                st.text(result_json_str) 
