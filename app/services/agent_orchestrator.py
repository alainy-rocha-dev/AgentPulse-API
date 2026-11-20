import json
import logging
from typing import Dict, Any, Optional, Callable
from app.services.tools import DeterministicTools
from app.services.repair_loop import RepairLoopService, SchemaValidationError
from app.schemas.agent_output import AnalysisOutputSchema
from app.services.llm_client import client_from_env

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """
    Orquestrador da cadeia de agentes de IA com suporte a ferramentas determinísticas e repair loop.
    """

    STUB_LABEL = "stub (no API key)"

    def __init__(self, llm_client: Optional[Callable[[str], str]] = None, use_env_llm: bool = True):
        """
        llm_client: qualquer função prompt -> str. Se omitido, usa o LLM configurado no ambiente
            (GROQ_API_KEY ou OPENAI_API_KEY) e, sem chave, o stub embutido.
        """
        if llm_client is None and use_env_llm:
            llm_client = client_from_env()
        self.llm_client = llm_client or self._default_llm_client
        self.model_label = getattr(llm_client, "label", None) if llm_client else self.STUB_LABEL
        self.last_attempt_errors: list = []

    def run_task(self, task_type: str, payload: Dict[str, Any]) -> AnalysisOutputSchema:
        logger.info(f"Iniciando orquestração de agentes para tipo '{task_type}'")

        # 1. Executar ferramentas determinísticas em itens/cláusulas do payload
        items = payload.get("items", [
            {"issue": "Sem penalidade de mora explícita", "severity": "HIGH"},
            {"issue": "Prazo de vigência sem aviso prévio", "severity": "MEDIUM"}
        ])
        calculated_metrics = DeterministicTools.calculate_risk_score(items)
        self._current_metrics = calculated_metrics

        # 2. Construir prompt para a cadeia de agentes
        prompt = (
            f"Você é um agente de análise de tarefas ({task_type}).\n"
            f"Analise o seguinte payload: {json.dumps(payload)}\n"
            f"Métricas determinísticas calculadas: {json.dumps(calculated_metrics)}\n\n"
            f"Retorne um JSON estrito com os campos: summary (texto), key_findings (lista de textos) "
            f"e metrics. O campo metrics deve repetir exatamente as métricas calculadas acima; "
            f"não recalcule nem altere nenhum número.\n"
            f"Exemplo de resposta esperada:\n"
            f"{{\n"
            f'  "summary": "Análise da tarefa concluída.",\n'
            f'  "key_findings": ["Achado 1", "Achado 2"],\n'
            f'  "metrics": {json.dumps(calculated_metrics)}\n'
            f"}}"
        )

        # 3. Disparar Repair Loop com Pydantic Schema Validation
        repair_service = RepairLoopService(llm_client=self.llm_client, max_attempts=3)
        try:
            result = repair_service.execute_with_repair(
                prompt, expected_metrics=calculated_metrics, model_label=self.model_label
            )
        finally:
            self.last_attempt_errors = list(repair_service.attempt_errors)

        logger.info(
            f"Orquestração concluída com sucesso para '{task_type}'. "
            f"Tentativas de reparo: {result.metadata.repair_attempts}, "
            f"Tempo total: {result.metadata.execution_time_seconds}s, "
            f"Score: {result.metrics.total_score} ({result.metrics.risk_level})"
        )
        return result

    def _default_llm_client(self, prompt: str) -> str:
        """Simulação default de LLM para ambiente sem chave de API."""
        # Retorna JSON formatado perfeitamente
        return json.dumps({
            "summary": "Análise orquestrada executada com sucesso.",
            "key_findings": [
                "Cláusula de rescisão validada",
                "Conformidade regulatória confirmada"
            ],
            # O stub repete as métricas calculadas, como um LLM bem-comportado faria.
            "metrics": getattr(self, "_current_metrics", None) or {
                "total_score": 65.0,
                "risk_level": "MEDIUM",
                "calculated_items": 2
            },
        })
