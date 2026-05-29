import pdfplumber
from io import BytesIO


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract all text from an uploaded PDF file."""
    try:
        bytes_data = uploaded_file.read()
        with pdfplumber.open(BytesIO(bytes_data)) as pdf:
            pages = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)
            return "\n\n".join(pages)
    except Exception as e:
        raise ValueError(f"Could not read PDF '{uploaded_file.name}': {e}")
