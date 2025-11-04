# 🚀 PathwayAgent

**PathwayAgent** is an AI-powered assistant designed to help students review and improve their **CV** and **Statement of Purpose (SOP)** with a focus on specific admission contexts—starting with *Institut Polytechnique de Paris (IP Paris)*. The system ensures **reliable, anonymized, and trustworthy feedback** using a modular, agent-based architecture.

---

## 🎯 Project Goal

Provide contextual and multi-agent feedback on CV and SOP files (PDF/Word), ensuring:

- Anonymization of sensitive information
- Alignment with target institution guidelines (e.g., IP Paris)
- Detailed feedback on grammar, structure, logic, and content alignment

---

## 🛠 Tools & Stack

| Component      | Tool/Library         |
|----------------|----------------------|
| Backend        | Python               |
| Grammar Checker |    Gramformer       | 
| LLM Framework  | LangChain            |
| NLP Models     | OpenAI API (initially), HuggingFace (later for open-source options) |
| PDF/Doc Reader | PyMuPDF              |
| UI             | Streamlit / Gradio   |
| Dataset        | Real or synthetic SOPs and CVs (anonymized or fake examples) |

---

## ❌ No Model Training Required

PathwayAgent **does not require model training**.

Instead, it leverages:

- **Pretrained LLMs** (e.g., OpenAI GPT-4, Claude, Mistral)
- **LangChain agents** to orchestrate modular tasks
- **Context injection** to guide feedback (e.g., IP Paris guidelines, SOP writing rules)
- **Prompt engineering** to simulate domain-aware expert feedback (few-shot prompting or CoTs...)

This makes the system:
- Lightweight and fast to prototype
- Easily extendable to other universities or programs
- Maintains high reliability and explainability

---

## 📌 Project Roadmap

### ✅ **Step 1: Document Parsing & Anonymization**

- **Input support**: Accept `.pdf` and `.docx` files for CV and SOP
- **Text extraction**: Use `PyMuPDF` to extract content
- **Anonymization** (initial naive version):
  - Regex-based masking of:
    - Names
    - Phone numbers
    - Email addresses
    - Physical addresses

> ⚠️ Will later explore Named Entity Recognition (NER) for more robust anonymization or LLM.

---

### 🚧 **Step 2: Multi-Agent Feedback with LangChain**

- **LangChain Agents**:
  - Modular agents performing specific review tasks
  - Use tools or chains (e.g., grammar corrector, logic checker)

- **Agents to include**:
  - 📝 **Grammar & Style Agent**
  - 🔗 **Logic & Coherence Agent**
  - 🎯 **Guideline Alignment Agent**:
    - Inject IP Paris admission requirements as *context*
    - Highlight missing or misaligned sections
    - Provide explanations with improvement suggestions

---

### 🔜 **Step 3: (Future Enhancements)**

- interactive inteview with LLM as jury for preparing motivation interview
- Feedback rating mechanism
- NER-based anonymization (Spacy / HF pipelines)
- Open-source model backend (e.g., Mistral, LLaMA2, Mixtral)
- Feedback summary generator
- Personalization using applicant metadata

---

## 📂 Dataset Strategy

- Start with real or fake CV/SOPs from past use
- No training or fine-tuning needed
- Sample scenarios can be manually crafted for evaluation and testing

---

## 📺 User Interface (UI)

Prototyped using **Streamlit** or **Gradio**.

Key features:
- Upload CV and SOP (PDF or Word)
- Preview anonymized content
- See feedback from multiple agents
- Download reviewed version

---

## 🎓 Use Case: IP Paris Admission

Guideline-aware feedback ensures your SOP:

- Highlights your research motivation, project alignment, and academic strength
- Reflects IP Paris core values (innovation, excellence, leadership)
- Avoids vague statements and redundant phrases
- Is grammatically correct, well-structured, and impactful

---
