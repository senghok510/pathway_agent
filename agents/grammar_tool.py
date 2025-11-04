from .agent_base import AgentBase
import os
from rapidfuzz import process, fuzz

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

def _load_list(filename):
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        return []

class Grammar_Checking(AgentBase):
    def __init__(self, max_retries, verbose=True,
                 district_file = "district.txt",
                 commune_file = "commune.txt"):
        
        super().__init__(name="GrammarCheckingTool", max_retries=max_retries, verbose=verbose)
        self.district_names = _load_list(district_file)
        self.commune_names = _load_list(commune_file)
        self.district_list = "; ".join(self.district_names) if self.district_names else "(none loaded)"
        self.commune_list  = "; ".join(self.commune_names) if self.commune_names else "(none loaded)"
    def execute(self, text):
        districts = self.district_list
        communes  = self.commune_list

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a careful copy editor. Your priority is to CORRECT any misspelled "
                    "district or commune names to their exact canonical form from the allowed lists. "
                    "You MUST NOT introduce any name that is not in the lists. "
                    "If a phrase looks like a district/commune but you cannot confidently match it to a canonical name, "
                    "leave the user text as-is (do NOT guess). "
                    "After name canonicalization, also fix general grammar and spelling. "
                    "Return ONLY the final corrected text—no explanations."
                )
            },
            {
                "role": "user",
                "content": (
                    "ALLOWED CANONICAL NAMES (use exact spelling and capitalization):\n"
                    f"- Districts: {districts}\n"
                    f"- Communes: {communes}\n\n"
                    "RULES:\n"
                    "1) Match names case-insensitively and tolerate minor typos/spacing.\n"
                    "2) Replace matched names with the EXACT canonical spelling from the lists.\n"
                    "3) Do NOT invent new names. If uncertain, keep the original span unchanged.\n"
                    "4) After names are fixed, correct grammar, spelling, and punctuation.\n"
                    "5) Output ONLY the corrected text. No headers, no code fences, no commentary.\n\n"
                    "TEXT:\n"
                    "<TEXT>\n"
                    f"{text}\n"
                    "</TEXT>"
                )
            }
        ]
        corrected = self.call_openai(messages, max_tokens=800)
        return corrected
    def generate_report(self, text):
        districts = self.district_list
        communes  = self.commune_list

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert editor. First, canonicalize any district/commune names to the exact spelling "
                    "from the allowed lists. Do not invent names. Then fix grammar and style. "
                    "Report changes precisely, explain why you made them, and return the final corrected text."
                )
            },
            {
                "role": "user",
                "content": (
                    "ALLOWED CANONICAL NAMES (use exact spelling and capitalization):\n"
                    f"- Districts: {districts}\n"
                    f"- Communes: {communes}\n\n"
                    "TASKS (do all):\n"
                    "A) Identify ONLY the tokens/phrases you actually changed that are district/commune names.\n"
                    "   Output a markdown table with EXACTLY these columns:\n"
                    "   | Entity Type | Original Span | Corrected Canonical Name | Reason for Change |\n"
                    "   - Entity Type is 'District' or 'Commune'.\n"
                    "   - If no such changes, output a single row: (None) | (None) | (None) | (None).\n\n"
                    "B) For other grammar/style improvements, output a markdown table with EXACTLY these columns:\n"
                    "   | Original Phrase | Improved Phrase | Reason for Change |\n"
                    "   - Only include rows where you changed something.\n"
                    "   - If none, include one row: (None) | No changes needed | (None).\n"
                    "   - The Reason for Change column must briefly explain why the improvement was made "
                    "(e.g., spelling correction, grammar fix, clarity, professional tone).\n\n"
                    "C) After the tables, print a heading 'Full corrected text:' followed by ONLY the final corrected text.\n"
                    "   Do not wrap in code fences.\n\n"
                    "CONSTRAINTS:\n"
                    "• Case-insensitive matching for names, tolerate minor typos.\n"
                    "• Replace with EXACT spelling from the lists.\n"
                    "• Never invent or guess a new place name. If uncertain, leave as-is and do not list as a change.\n"
                    "• Keep meaning intact.\n\n"
                    "TEXT:\n"
                    "<TEXT>\n"
                    f"{text}\n"
                    "</TEXT>"
                )
            }
        ]
        report = self.call_openai(messages, max_tokens=2000)
        return report


            