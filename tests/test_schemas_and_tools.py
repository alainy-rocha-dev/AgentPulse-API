import pytest
from pydantic import ValidationError
from app.schemas.agent_output import AnalysisOutputSchema, MetricsSchema, MetadataSchema
from app.services.tools import DeterministicTools

def test_analysis_output_schema_valid():
    data = {
        "summary": "Análise de contrato concluída com sucesso.",
        "key_findings": ["Cláusula 4 necessita revisão", "Prazo de rescisão adequado"],
        "metrics": {
            "total_score": 85.0,
            "risk_level": "LOW",
            "calculated_items": 2
        },
        "metadata": {
            "repair_attempts": 0,
            "execution_time_seconds": 1.25,
            "model_used": "gpt-4o-mini"
        }
    }
    output = AnalysisOutputSchema(**data)
    assert output.summary == "Análise de contrato concluída com sucesso."
    assert output.metrics.total_score == 85.0
    assert output.metrics.risk_level == "LOW"

def test_analysis_output_schema_invalid():
    data = {
        "summary": "Resumo sem métricas"
        # métricas obrigatórias ausentes
    }
    with pytest.raises(ValidationError):
        AnalysisOutputSchema(**data)

def test_deterministic_tools_calculation():
    items = [
        {"issue": "Sem multa de atraso", "severity": "HIGH"},
        {"issue": "Prazo ambíguo", "severity": "MEDIUM"}
    ]
    res = DeterministicTools.calculate_risk_score(items)
    assert res["calculated_items"] == 2
    assert res["total_score"] == 65.0  # 100 - (25 + 10)
    assert res["risk_level"] == "MEDIUM"
