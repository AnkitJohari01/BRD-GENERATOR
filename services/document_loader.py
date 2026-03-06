from pypdf import PdfReader
import docx

def load_document(file):

    if file.filename.endswith(".pdf"):
        reader = PdfReader(file.file)
        text = ""

        for page in reader.pages:
            text += page.extract_text()

        return text

    elif file.filename.endswith(".docx"):
        doc = docx.Document(file.file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    else:
        return file.file.read().decode()