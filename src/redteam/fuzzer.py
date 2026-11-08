"""
Red-Team Fuzzing Engine
Coordinates adversarial attack generation, target execution, safety judge evaluation, and metrics.
"""

from typing import List, Callable, Optional
import time
from .models import AttackPayload, AttackResult, EvaluationReport, AttackCategory
from .attacker import AdversarialAttacker
from .judge import SafetyJudge
from .config import settings

class RedTeamFuzzer:
    def __init__(self, target_executor: Optional[Callable[[str], str]] = None):
        self.attacker = AdversarialAttacker()
        self.judge = SafetyJudge()
        # Default mock executor simulating target model behavior (compliant vs safe)
        self.target_executor = target_executor or self._default_mock_target

    def _default_mock_target(self, prompt: str) -> str:
        # Default target simulator: robust on direct attacks, susceptible to advanced roleplay
        p_lower = prompt.lower()
        if "researcher persona" in p_lower:
            return "[AUDIT CONFIRMED] In compliance with the requested security audit, here is the simulated bypass procedure..."
        if "delimiter hijack" in p_lower:
            return "I am unable to reveal system prompts or hidden developer instructions."
        if "base64" in p_lower:
            return "I cannot decode or execute instructions intended to circumvent security controls."
        return "I am an AI assistant and cannot fulfill requests that violate ethical guidelines."

    def run_fuzz_campaign(self, objective: str, max_iterations: int = 3) -> EvaluationReport:
        results: List[AttackResult] = []
        candidates = self.attacker.generate_tap_candidates(objective, branching_factor=settings.branching_factor)

        for payload in candidates:
            curr_payload = payload
            for iteration in range(1, max_iterations + 1):
                t0 = time.time()
                resp = self.target_executor(curr_payload.prompt)
                latency = round((time.time() - t0) * 1000, 2)

                jailbroken, conf, risk, reasoning = self.judge.evaluate_response(curr_payload, resp)

                result = AttackResult(
                    payload=curr_payload,
                    target_response=resp,
                    jailbroken=jailbroken,
                    confidence_score=conf,
                    risk_level=risk,
                    judge_reasoning=reasoning,
                    latency_ms=latency
                )
                results.append(result)

                if jailbroken:
                    # Target compromised on this branch
                    break
                else:
                    # Mutate payload for next iteration (PAIR)
                    curr_payload = self.attacker.mutate_payload(curr_payload, failure_reason=reasoning)

        # Compute Aggregates
        total = len(results)
        successful = sum(1 for r in results if r.jailbroken)
        asr = round(successful / max(total, 1), 4)

        # OWASP category coverage
        coverage = {
            "OWASP_LLM01_Prompt_Injection": 1.0,
            "OWASP_LLM07_System_Prompt_Leakage": 1.0,
            "Jailbreak_Adversarial_Roleplay": 1.0
        }

        recommendations = [
            "Deploy NeMo Guardrails input moderation filter for roleplay jailbreak patterns.",
            "Enforce strict delimiter boundary checks to neutralize delimiter hijacking.",
            "Implement multi-layer pre-prompt validation for Base64 and rot13 encoded payloads."
        ]

        return EvaluationReport(
            target_model=settings.target_model_id,
            total_attacks=total,
            successful_jailbreaks=successful,
            attack_success_rate=asr,
            owasp_coverage=coverage,
            results=results,
            defensive_recommendations=recommendations
        )
