import streamlit as st
import requests

st.set_page_config(
    page_title="LegalEase AI",
    page_icon="⚖️"
)

st.title("⚖️ LegalEase AI")
st.subheader("AI-Based Legal Document Generator")

st.write(
    "Generate legal document drafts easily using AI."
)

document_type = st.selectbox(
    "Select Document Type",
    [
        "Rental Agreement",
        "Employment Agreement",
        "Non-Disclosure Agreement",
        "Service Agreement"
    ]
)

party1 = st.text_input("First Party Name")
party2 = st.text_input("Second Party Name")
terms = st.text_area("Terms and Conditions")
effective_date = st.date_input("Effective Date")

if st.button("Generate Document"):

    if party1 and party2 and terms:

        data = {
            "document_type": document_type,
            "party1": party1,
            "party2": party2,
            "terms": terms,
            "effective_date": str(effective_date)
        }

        try:
            with st.spinner("Generating your document..."):

                response = requests.post(
                    "http://127.0.0.1:8000/generate",
                    json=data,
                    timeout=120
                )

            if response.status_code == 200:

                document = response.json()["document"]

                st.success("Document Generated Successfully!")

                st.subheader("Generated Legal Document")

                st.text_area(
                    "Your Document",
                    document,
                    height=500
                )

                st.download_button(
                    "Download Document",
                    data=document,
                    file_name="LegalEase_Document.txt",
                    mime="text/plain"
                )

            else:
                st.error(f"Error: {response.text}")

        except requests.RequestException as e:
            st.error(f"Connection Error: {e}")

    else:
        st.warning("Please fill all fields.")