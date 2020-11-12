"""
Very basic out-of-the-box example using the full visualizer. This file can be
run using the "streamlit run" command.

Prerequisites:
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
"""

# Need to add streamlit app
import spacy
import streamlit as st
from spacy_streamlit import visualize_ner

nlp = spacy.load("en_core_web_md")

txt = st.text_area('Text to analyze', 'Input Text Goes Here')
doc = nlp(txt)
visualize_ner(doc, labels=nlp.get_pipe("ner").labels)