from .agent_base import AgentBase
import re
import pdfplumber
from textwrap import shorten

ANON_TAG_PATTERN = re.compile(r"<([A-Z_]+)>")

class CVRecommenderAgent(AgentBase):
    def __init__(self, guideline_pdf_path, max_retries=2, verbose=True, guideline_max_chars=12000):
        super().__init__(name="CVRecommenderAgent", max_retries=max_retries, verbose=verbose)
        full_guideline = self._extract_guideline_text(guideline_pdf_path)
        self.guideline_text = shorten(full_guideline, width=guideline_max_chars, placeholder="\n...[truncated]...")

    def _extract_guideline_text(self, pdf_path):
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                pg_txt = page.extract_text() or ""
                text += pg_txt + "\n"
        return text

    def _collect_anonymized_presence(self, cv_text):
        counts = {}
        for m in ANON_TAG_PATTERN.finditer(cv_text):
            tag = m.group(1)
            counts[tag] = counts.get(tag, 0) + 1
        return counts
    def execute(self, cv_text):
        anon_counts = self._collect_anonymized_presence(cv_text)
        anon_summary = ", ".join(f"{k}:{v}" for k,v in anon_counts.items()) if anon_counts else "none"

        format_instructions = (
            "OUTPUT FORMAT REQUIREMENTS (strict):\n"
            "For each logical CV section (e.g., Header, Objective/Summary, Education, Experience, Projects, Skills, "
            "Achievements/Awards, Activities/Leadership, Certifications, Languages, Additional/Other), produce a block in this exact shape:\n\n"
            "## **<Section Name>**  (Click to load recommendations)\n"
            "**Original:**\n"
            "[original text OR 'Not present']\n"
            "**Recommended:**\n"
            ">>> paste-ready improved content (concise; keep placeholders intact). If no change, write: '✅ No change needed'. <<<\n"
            "**Why this change:**\n"
            "- Reason 1 (e.g., clarity, quantification, structure, consistency)\n"
            "- Reason 2 (e.g., stronger verbs, metrics, ordering)\n"
            "---\n\n"
            "If a section is missing, add ' (Missing)' immediately after the section name and provide a recommended version.\n"
            "If removing weak content, include: (Remove: brief reason) inside the Recommended block.\n\n"
            "STYLE RULES:\n"
            "- Never ask to add data already represented by placeholders (<PERSON>, <EMAIL_ADDRESS>, <PHONE_NUMBER>, <DISTRICT>, <COMMUNE>, <LOCATION>).\n"
            "- Respect placeholders exactly; do not expand, reveal, or invent personal data.\n"
            "- Be specific: quantify impact; use strong action verbs; tighten wording; keep formatting consistent.\n"
            "- Preserve factual meaning; do not fabricate achievements or employers.\n"
            "- Bullets (if used) start with a verb and (where possible) include metrics/scope.\n"
            "- Avoid repeating the same soft skills across multiple bullets unless context differs.\n"
            "- No code fences, no JSON wrappers.\n\n"
            "FINAL SECTIONS (mandatory):\n"
            "## **Suggested CV Structure**  (Click to load recommendations)\n"
            "**Original:**\n"
            "[Detected ordering summary]\n"
            "**Recommended:**\n"
            ">>> List ideal ordered section names (and any optional items) <<<\n"
            "---\n\n"
            "## **Rewritten CV (placeholders preserved)**\n"
            "[BEGIN_REWRITTEN_CV]\n"
            "- Produce a single cohesive CV that integrates all your 'Recommended' content above in the 'Suggested CV Structure' order.\n"
            "- Keep all placeholders exactly as they appear (e.g., <PERSON>, <EMAIL_ADDRESS>). Do not replace or reveal them.\n"
            "- Maintain clean, professional formatting (headings and bullets) suitable for direct copy-paste.\n"
            "- Do NOT include 'Why this change' notes here.\n"
            "[END_REWRITTEN_CV]\n"
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert CV reviewer and formatter. The CV text provided is ANONYMIZED: placeholders like "
                    "<PERSON>, <EMAIL_ADDRESS>, <PHONE_NUMBER>, <DISTRICT>, <COMMUNE>, <LOCATION> signify that real data "
                    "is present but masked. Never suggest adding information already indicated by a placeholder. Focus on: "
                    "structure, missing sections, measurable impact, clarity, ordering, concision, consistency, and alignment "
                    "with professional standards and the supplied guideline. Be actionable and concise."
                )
            },
            {
                "role": "user",
                "content": (
                    "Guideline Reference (for identifying gaps / best practices):\n"
                    f"{self.guideline_text}\n\n"
                    f"Anonymization placeholders detected (token:count): {anon_summary}\n\n"
                    "Anonymized CV Text:\n"
                    f"{cv_text}\n\n"
                    f"{format_instructions}"
                )
            }
        ]
        recommendations = self.call_openai(messages, max_tokens=2200)
        return recommendations

