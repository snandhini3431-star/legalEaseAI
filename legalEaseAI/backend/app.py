
import streamlit as st
import requests
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch


# Page Configuration
st.set_page_config(
    page_title="LegalEase AI",
    page_icon="⚖️",
    layout="centered"
)


# Application Title
st.title("⚖️ LegalEase AI")

st.subheader("AI-Based Legal Document Generator")

st.write(
    "Generate legal document drafts easily using Artificial Intelligence."
)

st.divider()


# Document Type
document_type = st.selectbox(
    "Select Document Type",
    [
        "Rental Agreement",
        "Employment Agreement",
        "Non-Disclosure Agreement",
        "Service Agreement"
    ]
)


# User Inputs
party1 = st.text_input(
    "First Party Name",
    placeholder="Enter first party name"
)

party2 = st.text_input(
    "Second Party Name",
    placeholder="Enter second party name"
)

terms = st.text_area(
    "Terms and Conditions",
    placeholder="Enter agreement terms here...",
    height=150
)

effective_date = st.date_input(
    "Effective Date"
)


st.divider()


# Generate Document Button
if st.button("Generate Document", type="primary"):

    if not party1.strip() or not party2.strip() or not terms.strip():

        st.warning("Please fill all fields.")

    else:

        data = {
            "document_type": document_type,
            "party1": party1,
            "party2": party2,
            "terms": terms,
            "effective_date": str(effective_date)
        }

        try:

            with st.spinner("AI is generating your document..."):

                response = requests.post(
                    "http://127.0.0.1:8000/generate",
                    json=data,
                    timeout=180
                )

            if response.status_code == 200:

                document = response.json().get("document", "")

                if not document:
                    st.error("No document was returned by the AI.")
                    st.stop()

                st.success("Document Generated Successfully!")

                st.divider()

                st.header("Generated Legal Document")

                # Display Document
                st.text_area(
                    "Your Document",
                    value=document,
                    height=500
                )

                # TXT Download
                st.download_button(
                    label="Download TXT",
                    data=document,
                    file_name="LegalEase_Document.txt",
                    mime="text/plain"
                )

                # Create PDF
                pdf_buffer = BytesIO()

                pdf = SimpleDocTemplate(
                    pdf_buffer,
                    pagesize=A4,
                    rightMargin=inch,
                    leftMargin=inch,
                    topMargin=inch,
                    bottomMargin=inch
                )

                styles = getSampleStyleSheet()

                story = []

                story.append(
                    Paragraph(
                        "LegalEase AI - Legal Document Draft",
                        styles["Title"]
                    )
                )

                story.append(Spacer(1, 20))

                # Add document text with wrapping
                for line in document.splitlines():

                    if line.strip():

                        story.append(
                            Paragraph(
                                escape(line),
                                styles["BodyText"]
                            )
                        )

                        story.append(Spacer(1, 6))

                    else:

                        story.append(Spacer(1, 10))

                pdf.build(story)

                # PDF Download
                st.download_button(
                    label="Download PDF",
                    data=pdf_buffer.getvalue(),
                    file_name="LegalEase_Document.pdf",
                    mime="application/pdf"
                )

                st.info(
                    "This AI-generated document is a draft. "
                    "Please consult a qualified lawyer before signing."
                )

            else:

                st.error(
                    f"Server Error: {response.status_code}"
                )

                st.code(response.text)

        except requests.exceptions.Timeout:

            st.error(
                "The AI is taking too long. Please try again."
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to backend. "
                "Please check whether FastAPI is running."
            )

        except Exception as e:

            st.error(f"Unexpected Error: {e}")


st.divider()

st.caption("LegalEase AI | AI-Based Legal Document Draft Generator")