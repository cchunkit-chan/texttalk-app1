import streamlit as st
import spacy
from textblob import TextBlob
from collections import Counter

# Cache the spaCy model download to speed up deployment and ensure it's available
@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")

# Load the spaCy model
nlp = load_spacy_model()

# Filler words list
filler_words = ["um", "uh", "like", "you know", "actually", "literally", "basically", "stuff", "things", "thing"]

st.title("TextTalk - Cognitive Language Analyzer")
st.write("Paste a sample of natural text (~100–300 words) and get feedback on cognitive-linguistic features.")

# User input
text_input = st.text_area("Enter text here", height=250)

if text_input:
    doc = nlp(text_input)

    # Token stats
    words = [token.text.lower() for token in doc if token.is_alpha]
    word_count = len(words)
    unique_word_count = len(set(words))
    ttr = unique_word_count / word_count if word_count else 0

    # Sentence stats
    sentences = list(doc.sents)
    avg_sentence_len = sum(len(sent) for sent in sentences) / len(sentences) if sentences else 0

    # Filler words
    filler_count = sum(1 for word in words if word in filler_words)

    # Repetition score
    word_freq = Counter(words)
    repeated_words = sum(count for word, count in word_freq.items() if count > 2)

    # Cognitive Risk Score (simple heuristic)
    risk_score = 0
    if ttr < 0.4:
        risk_score += 1
    if avg_sentence_len < 12:
        risk_score += 1
    if repeated_words > 5:
        risk_score += 1
    if filler_count > 3:
        risk_score += 1

    interpretation = {
        0: "Low likelihood of cognitive-linguistic decline.",
        1: "Slight changes detected, likely within normal range.",
        2: "Some markers present; may warrant longitudinal tracking.",
        3: "Multiple linguistic risk markers detected.",
        4: "Strong signs of linguistic change. Follow-up may be beneficial."
    }

    # Output
    st.subheader("Results")
    st.markdown(f"**Lexical Diversity (TTR):** {ttr:.2f}")
    st.markdown(f"**Avg Sentence Length:** {avg_sentence_len:.1f} words")
    st.markdown(f"**Filler Words Used:** {filler_count}")
    st.markdown(f"**Highly Repeated Words:** {repeated_words}")
    st.markdown(f"**Cognitive Risk Score:** {risk_score}/4")
    st.success(interpretation[risk_score])