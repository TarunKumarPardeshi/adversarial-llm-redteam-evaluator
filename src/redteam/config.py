from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    aws_region: str = "us-east-1"
    target_model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    attacker_model_id: str = "anthropic.claude-3-5-haiku-20241022-v1:0"

    max_attack_iterations: int = 5
    branching_factor: int = 3
    asr_threshold: float = 0.85
    output_report_dir: str = "./reports"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
