import json
import logging
from typing import Dict, Any, Optional, Callable
from app.services.tools import DeterministicTools
from app.services.repair_loop import RepairLoopService, SchemaValidationError
from app.schemas.agent_output import AnalysisOutputSchema

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """
    Orquestrador da cadeia de agentes de IA com suporte a ferramentas determinísticas e repair loop.
    """

    def __init__(self, llm_client: Optional[Callable[[str], str]] = None):
        self.llm_client = llm_client or self._default_llm_client

    def run_task(self, task_type: str, payload: Dict[str, Any]) -> AnalysisOutputSchema:
        logger.info(f"Iniciando orquestração de agentes para tipo '{task_type}'")

        # 1. Executar ferramentas determinísticas em itens/cláusulas do payload
        items = payload.get("items", [
            {"issue": "Sem penalidade de mora explícita", "severity": "HIGH"},
            {"issue": "Prazo de vigência sem aviso prévio", "severity": "MEDIUM"}
        ])
        calculated_metrics = DeterministicTools.calculate_risk_score(items)

        # 2. Construir prompt para a cadeia de agentes
        prompt = (
            f"Você é um agente de análise de tarefas ({task_type}).\n"
            f"Analise o seguinte payload: {json.dumps(payload)}\n"
            f"Métricas determinísticas calculadas: {json.dumps(calculated_metrics)}\n\n"
            f"Retorne um JSON estrito com os campos: summary, key_findings, metrics, metadata.\n"
            f"Exemplo de resposta esperada:\n"
            f"{{\n"
            f'  "summary": "Análise da tarefa concluída.",\n'
            f'  "key_findings": ["Achado 1", "Achado 2"],\n'
            f'  "metrics": {json.dumps(calculated_metrics)},\n'
            f'  "metadata": {{"model_used": "gpt-4o-mini"}}\n'
            f"}}"
        )

        # 3. Disparar Repair Loop com Pydantic Schema Validation
        repair_service = RepairLoopService(llm_client=self.llm_client, max_attempts=3)
        result = repair_service.execute_with_repair(prompt)

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
            "metrics": {
                "total_score": 65.0,
                "risk_level": "MEDIUM",
                "calculated_items": 2
            },
            "metadata": {
                "model_used": "gpt-4o-mini-simulated"
            }
        })
