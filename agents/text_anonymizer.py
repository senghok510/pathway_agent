from .agent_base import AgentBase
from presidio_analyzer import PatternRecognizer, RecognizerRegistry, AnalyzerEngine
import os

ALLOWED_ENTITIES = ["PERSON", "LOCATION", "EMAIL_ADDRESS", "PHONE_NUMBER", "DISTRICT", "COMMUNE"] 


class Text_anonymizer(AgentBase):
    def __init__(self):
        super().__init__(name="Anonymizer_tool")
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        with open(os.path.join(base_dir, "district.txt"), "r") as f:
            district_names = [line.strip() for line in f if line.strip()]
        self.district_recognizer = PatternRecognizer(supported_entity="LOCATION", deny_list=district_names)
        with open(os.path.join(base_dir, "commune.txt"), "r") as f:
            commune_names = [line.strip() for line in f if line.strip()]
        self.commune_recognizer = PatternRecognizer(supported_entity="LOCATION", deny_list=commune_names)

    def _select_best_non_overlapping(self, results):
        sorted_results = sorted(results, key=lambda r: (-r.score, -(r.end - r.start), r.start))
        chosen = []
        for cand in sorted_results:
            overlaps = any( not (cand.end <= kept.start or cand.start >= kept.end) for kept in chosen)
            if not overlaps:
                chosen.append(cand)
        return sorted(chosen, key=lambda r: r.start)
    
    def _replace_with_entities(self, text, results):
        parts = []
        cursor = 0
        for r in results:
            parts.append(text[cursor:r.start])
            parts.append(f"<{r.entity_type}>")
            cursor = r.end
        parts.append(text[cursor:])
        return "".join(parts)

    def execute(self, text):
        registry = RecognizerRegistry()
        registry.load_predefined_recognizers()
        registry.add_recognizer(self.district_recognizer)
        registry.add_recognizer(self.commune_recognizer)
        analyzer = AnalyzerEngine(registry=registry)
        results = analyzer.analyze(text=text, language="en", entities=ALLOWED_ENTITIES)
        best = self._select_best_non_overlapping(results)
        final_text = self._replace_with_entities(text, best)
        return final_text