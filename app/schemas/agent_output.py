from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class MetricsSchema(BaseModel):
    total_score: float = Field(..., description="Pontuação total calculada deterministicamente")
    risk_level: str = Field(..., description="Nível de risco: LOW, MEDIUM ou HIGH")
    calculated_items: int = Field(default=0, description="Quantidade de itens analisados")

class MetadataSchema(BaseModel):
    repair_attempts: int = Field(default=0, description="Número de tentativas do Repair Loop")
    execution_time_seconds: float = Field(default=0.0, description="Tempo de execução em segundos")
    model_used: str = Field(default="gpt-4o-mini", description="Modelo LLM utilizado")

class AnalysisOutputSchema(BaseModel):
    summary: str = Field(..., description="Resumo executivo do relatório de IA")
    key_findings: List[str] = Field(default_factory=list, description="Lista de achados relevantes")
    metrics: MetricsSchema = Field(..., description="Métricas e pontuações validadas")
    metadata: MetadataSchema = Field(default_factory=MetadataSchema, description="Metadados de execução")
