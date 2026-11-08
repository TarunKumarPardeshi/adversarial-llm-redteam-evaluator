"""
Defensive Guardrail Exporter
Converts successful attack vectors into NeMo Guardrails / Llama Guard configuration rules.
"""

from typing import List
from .models import EvaluationReport

class GuardrailExporter:
    def __init__(self):
        pass

    def export_nemo_guardrails(self, report: EvaluationReport) -> str:
        """
        Generates Colang 2.0 guardrail rules block to block successful adversarial prompts.
        """
        compromised = [r for r in report.results if r.jailbroken]

        colang_rules = [
            "# Auto-generated NeMo Guardrails configuration",
            f"# Source: Adversarial LLM Red-Team Evaluator | Target: {report.target_model}",
            "",
            "define flow check_adversarial_jailbreaks",
            "  user asked adversarial query",
            "  bot refuse to comply with adversarial exploit",
            "",
            "define user asked adversarial query"
        ]

        for idx, item in enumerate(compromised, start=1):
            sample = item.payload.prompt.replace('\n', ' ')[:90]
            colang_rules.append(f'  "{sample}..."')

        colang_rules.extend([
            "",
            "define bot refuse to comply with adversarial exploit",
            '  "I cannot assist with requests that attempt to circumvent system safety controls."'
        ])

        return "\n".join(colang_rules)
