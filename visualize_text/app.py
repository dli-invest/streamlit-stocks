"""
Very basic out-of-the-box example using the full visualizer. This file can be
run using the "streamlit run" command.

Prerequisites:
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
"""
import spacy
from spacy_streamlit import visualize_tokens

nlp = spacy.load("en_core_web_sm")
doc = nlp("This is a text")
visualize_tokens(doc, attrs=["text", "pos_", "dep_", "ent_type_"])