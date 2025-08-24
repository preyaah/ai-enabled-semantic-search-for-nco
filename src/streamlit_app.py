import sys
import os

# Add project root to Python path first!
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.models.enhanced_search import EnhancedNCOSearch

# Initialize search engine once
@st.cache_resource
def load_search_engine():
    return EnhancedNCOSearch()

search_engine = load_search_engine()

st.title("🔍 NCO Semantic Search")

st.write("Enter a job description to find matching NCO occupation codes")

query = st.text_input("Job Description", "")

if st.button("Search NCO Codes") and query.strip():
    with st.spinner("Searching..."):
        results = search_engine.search(query, top_k=10)
    
    if results:
        st.success(f"Top matches for '{query}':")
        for i, res in enumerate(results, 1):
            st.markdown(f"**{i}. {res['occupation']}**")
            st.write(f"Confidence: {res['confidence_percent']}%")
            st.write("---")
    else:
        st.warning("No matching occupations found.")
