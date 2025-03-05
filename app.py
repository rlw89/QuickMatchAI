import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz

# Streamlit UI
st.title("Quick Match AI Tool")
st.write("Upload two CSV files and match data based on similarity.")

# File uploads
file1 = st.file_uploader("Upload First CSV", type=["csv"])
file2 = st.file_uploader("Upload Second CSV", type=["csv"])

if file1 and file2:
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    col1 = st.selectbox("Select Column from First CSV", df1.columns)
    col2 = st.selectbox("Select Column from Second CSV", df2.columns)
    
    threshold = st.slider("Matching Accuracy Threshold (0-100)", 0, 100, 80)
    
    if st.button("Match Data"):
        matches = []
        for index1, row1 in df1.iterrows():
            best_match = None
            highest_score = 0
            for index2, row2 in df2.iterrows():
                score = fuzz.ratio(str(row1[col1]), str(row2[col2]))
                if score > highest_score and score >= threshold:
                    highest_score = score
                    best_match = row2[col2]
            matches.append((row1[col1], best_match, highest_score))
        
        results_df = pd.DataFrame(matches, columns=["First CSV Data", "Matched Second CSV Data", "Match Score"])
        st.write(results_df)
        
        csv = results_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Matched Results", csv, "matched_results.csv", "text/csv")
