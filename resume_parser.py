from io import BytesIO

from docx import Document
from pypdf import PdfReader


def extract_pdf_text(uploaded_file):
    """Extract text from every page of a PDF resume."""

    uploaded_file.seek(0)

    reader = PdfReader(uploaded_file)

    pages = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            pages.append(page_text)

    return "\n".join(pages)


def extract_docx_text(uploaded_file):
    """Extract text from every paragraph of a DOCX resume."""

    uploaded_file.seek(0)

    file_bytes = BytesIO(uploaded_file.read())

    document = Document(file_bytes)

    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)


def extract_resume_text(uploaded_file):
    """Choose the correct method for PDF or DOCX resumes."""

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_pdf_text(uploaded_file)

    if file_name.endswith(".docx"):
        return extract_docx_text(uploaded_file)

    raise ValueError("Only PDF and DOCX files are supported.")