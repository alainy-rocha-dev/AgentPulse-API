import pytest
from app.services.repair_loop import RepairLoopService, SchemaValidationError
from app.schemas.agent_output import AnalysisOutputSchema

class MockLLMProvider:
    def __init__(self, responses):
        self.responses = responses
        self.call_count = 0

    def generate(self, prompt: str) -> str:
        resp = self.responses[min(self.call_count, len(self.responses) - 1)]
        self.call_count += 1
        return resp

def test_repair_loop_success_first_attempt():
    valid_json = '''
    {
        "summary": "Sucesso na 1ª tentativa",
        "key_findings": ["OK"],
        "metrics": {"total_score": 90.0, "risk_level": "LOW", "calculated_items": 1},
        "metadata": {"repair_attempts": 0, "execution_time_seconds": 0.5, "model_used": "mock"}
    }
    '''
    mock_llm = MockLLMProvider([valid_json])
    repair_service = RepairLoopService(llm_client=mock_llm.generate, max_attempts=3)
    result = repair_service.execute_with_repair("Analise o texto")
    
    assert isinstance(result, AnalysisOutputSchema)
    assert result.summary == "Sucesso na 1ª tentativa"
    assert mock_llm.call_count == 1

def test_repair_loop_success_second_attempt():
    invalid_json = '{"summary": "Faltando métricas"}'
    valid_json = '''
    {
        "summary": "Corrigido na 2ª tentativa",
        "key_findings": ["OK"],
        "metrics": {"total_score": 80.0, "risk_level": "LOW", "calculated_items": 1},
        "metadata": {"repair_attempts": 1, "execution_time_seconds": 1.0, "model_used": "mock"}
    }
    '''
    mock_llm = MockLLMProvider([invalid_json, valid_json])
    repair_service = RepairLoopService(llm_client=mock_llm.generate, max_attempts=3)
    result = repair_service.execute_with_repair("Analise o texto")

    assert isinstance(result, AnalysisOutputSchema)
    assert result.summary == "Corrigido na 2ª tentativa"
    assert result.metadata.repair_attempts == 1
    assert mock_llm.call_count == 2

def test_repair_loop_exhaustion():
    invalid_json = '{"invalid": "json"}'
    mock_llm = MockLLMProvider([invalid_json, invalid_json, invalid_json])
    repair_service = RepairLoopService(llm_client=mock_llm.generate, max_attempts=3)
    
    with pytest.raises(SchemaValidationError) as excinfo:
        repair_service.execute_with_repair("Analise o texto")

    assert "SchemaValidationError: Falha na validação do resultado após 3 tentativas" in str(excinfo.value)
    assert mock_llm.call_count == 3
