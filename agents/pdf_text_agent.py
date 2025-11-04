import pdfplumber
from .agent_base import AgentBase

class PDFTextAgent(AgentBase):
    def __init__(self):
        super().__init__(name="PDFTextAgent")

    def extract_text(self, pdf_path):
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                pg_txt = page.extract_text() or ""
                text += pg_txt + "\n"
        return text
