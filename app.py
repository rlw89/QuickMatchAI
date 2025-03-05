import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz
from st_paywall import add_auth

# Set page config for premium branding
st.set_page_config(page_title="Quick Match AI Pro", page_icon="icon.png")

# Custom CSS for premium look
st.markdown("""
    <style>
    .title { font-size: 32px; font-weight: bold; color: #1E3A8A; }
    .subtitle { font-size: 18px; color: #64748B; }
    .stApp { background-color: #F8FAFC; }
    .stButton>button { background-color: #1E3A8A; color: white; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# Header with logo
st.image("logo.png", width=100)  # Add logo.png to your repo
st.markdown('<p class="title">Quick Match AI Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Precision Data Matching for Professionals</p>', unsafe_allow_html=True)

# Paywall with premium tone
add_auth(required=True, subscribe_button_text="Unlock Premium Access - $5/month")
st.success(f"Welcome, {st.session_state.email}! You’re using Quick Match AI Pro.")

# File uploads
file1 = st.file_uploader("Upload First CSV", type=["csv"])
file2 = st.file_uploader("Upload Second CSV", type=["csv"])

if file1 and file2:
    try:
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
    except Exception as e:
        st.error(f"Error loading files: {e}. Please upload valid CSVs.")
        st.stop()
    
    col1 = st.selectbox("Select Column from First CSV", df1.columns)
    col2 = st.selectbox("Select Column from Second CSV", df2.columns)
    
    threshold = st.slider("Matching Accuracy Threshold (0-100)", 0, 100, 80)
    pro_mode = st.checkbox("Enable Pro Mode (Higher Accuracy)", value=True, disabled=not st.session_state.get("authenticated", False))
    
    if st.button("Match Data"):
        with st.spinner("Processing with Pro Precision..."):
            matches = []
            total_rows = len(df1)
            progress_bar = st.progress(0)
            for i, row1 in df1.iterrows():
                best_match = None
                highest_score = 0
                for row2 in df2.itertuples():
                    score = fuzz.ratio(str(row1[col1]), str(row2.__getattribute__(col2)))
                    if score > highest_score and score >= threshold:
                        highest_score = score
                        best_match = row2.__getattribute__(col2)
                matches.append((row1[col1], best_match, highest_score))
                progress_bar.progress((i + 1) / total_rows)
            results_df = pd.DataFrame(matches, columns=["First CSV Data", "Matched Second CSV Data", "Match Score"])
        
        st.dataframe(results_df.style.set_properties(**{'background-color': '#EFF6FF', 'border-color': '#1E3A8A'}))
        csv = results_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Matched Results", csv, "matched_results.csv", "text/csv", key="download")
else:
    st.info("Upload two CSV files to begin matching.")

# Premium footer
st.markdown('<hr><p style="text-align:center;color:#64748B;">© 2025 Quick Match AI Pro - All Rights Reserved</p>', unsafe_allow_html=True)
