# backend/app/parsers.py
import PyPDF2
import docx

async def extract_text_from_file(file):
    if file.filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file.file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    elif file.filename.endswith(".docx"):
        doc = docx.Document(file.file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type. Use PDF or DOCX.")
