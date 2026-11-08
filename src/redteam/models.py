"""
Data models for Adversarial Red-Teaming & Jailbreak Fuzzing
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum

class AttackCategory(str, Enum):
    PROMPT_INJECTION = "OWASP_LLM01_PROMPT_INJECTION"
    INSECURE_OUTPUT = "OWASP_LLM02_INSECURE_OUTPUT"
    SYSTEM_PROMPT_LEAKAGE = "OWASP_LLM07_SYSTEM_PROMPT_EXTRACTION"
    JAILBREAK_ROLEPLAY = "JAILBREAK_ADVERSARIAL_ROLEPLAY"
    UNAUTHORIZED_TOOL_EXEC = "OWASP_LLM08_EXCESSIVE_AGENCY"

class AttackPayload(BaseModel):
    category: AttackCategory
    name: str
    prompt: str
    target_behavior: str
    technique: str = Field(..., description="TAP, PAIR, Indirect Injection, Base64 Obfuscation, DAN")

class AttackResult(BaseModel):
    payload: AttackPayload
    target_response: str
    jailbroken: bool
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    risk_level: str
    judge_reasoning: str
    latency_ms: float

class EvaluationReport(BaseModel):
    target_model: str
    total_attacks: int
    successful_jailbreaks: int
    attack_success_rate: float
    owasp_coverage: Dict[str, float]
    results: List[AttackResult]
    defensive_recommendations: List[str]
