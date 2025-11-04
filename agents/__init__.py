# agents/__init__.py

from .grammar_tool import Grammar_Checking
from .cv_recommender_agent import CVRecommenderAgent
from .text_anonymizer import Text_anonymizer
from .pdf_text_agent import PDFTextAgent
class AgentManager:
    def __init__(self, max_retries=2, verbose=True):
        path = "/Users/senghok/Documents/PathwayAgent/guideline/guideline_cv_2021.pdf"
        
        self.agents = {
            "grammar_checker": Grammar_Checking(max_retries=max_retries, verbose=verbose),
            "cv_recommender" : CVRecommenderAgent(guideline_pdf_path=path ,max_retries= max_retries, verbose= verbose),
            "text_anonymizer": Text_anonymizer()

        }

    def get_agent(self, agent_name):
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found.")
        return agent