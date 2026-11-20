import json
import logging
import time
from typing import Callable, Any, Dict, List, Optional
from pydantic import ValidationError
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type

from app.schemas.agent_output import AnalysisOutputSchema

logger = logging.getLogger(__name__)

class SchemaValidationError(Exception):
    """Exceção customizada quando o Repair Loop atinge o limite de tentativas."""
    pass


class MetricsMismatchError(ValueError):
    """O LLM devolveu métricas diferentes das calculadas pelas ferramentas determinísticas."""
    pass

class RepairLoopService:
    """
    Serviço de Repair Loop Anti-Alucinação.
    Executa re-prompting com o erro do Pydantic se o LLM gerar um JSON malformado.
    """

    def __init__(self, llm_client: Callable[[str], str], max_attempts: int = 3):
        self.llm_client = llm_client
        self.max_attempts = max_attempts
        # Erro de cada tentativa rejeitada na última execução (usado na avaliação ao vivo).
        self.attempt_errors: List[str] = []

    def execute_with_repair(
        self,
        initial_prompt: str,
        expected_metrics: Optional[Dict[str, Any]] = None,
        model_label: Optional[str] = None,
    ) -> AnalysisOutputSchema:
        """
        Chama o LLM até obter um JSON válido.

        expected_metrics: métricas calculadas pelas ferramentas determinísticas. Se o LLM devolver
            valores diferentes, a resposta é rejeitada como qualquer outro erro de validação e o
            LLM recebe os valores corretos no re-prompt. Nenhum número alterado pelo LLM é salvo.
        model_label: modelo que realmente respondeu; substitui o que o LLM declarar em metadata.
        """
        current_prompt = initial_prompt
        last_error_msg = ""
        start_time = time.time()
        self.attempt_errors = []

        for attempt in range(1, self.max_attempts + 1):
            logger.info(f"Executando tentativa {attempt} de {self.max_attempts} no Repair Loop.")
            try:
                raw_response = self._call_llm_with_retry(current_prompt)
                
                # Tentar parsing de JSON e validação via Pydantic
                json_data = json.loads(raw_response)
                validated_output = AnalysisOutputSchema(**json_data)
                if expected_metrics is not None:
                    self._check_metrics(validated_output, expected_metrics)
                
                # Atualizar metadados
                elapsed_time = round(time.time() - start_time, 2)
                validated_output.metadata.repair_attempts = attempt - 1
                validated_output.metadata.execution_time_seconds = elapsed_time
                if model_label:
                    validated_output.metadata.model_used = model_label

                logger.info(f"Resultado validado com sucesso na tentativa {attempt}.")
                return validated_output

            except (json.JSONDecodeError, ValidationError, MetricsMismatchError, TypeError) as exc:
                last_error_msg = str(exc)
                self.attempt_errors.append(f"{exc.__class__.__name__}: {last_error_msg[:300]}")
                logger.warning(f"Tentativa {attempt} falhou na validação: {last_error_msg}")
                
                if attempt < self.max_attempts:
                    current_prompt = (
                        f"{initial_prompt}\n\n"
                        f"[AVISO DE ERRO DE VALIDAÇÃO PYDANTIC]:\n"
                        f"Sua resposta anterior foi rejeitada com o seguinte erro:\n{last_error_msg}\n\n"
                        f"Por favor, corrija a estrutura do JSON e devolva APENAS um JSON válido compatível com o schema esperado."
                    )

        raise SchemaValidationError(
            f"SchemaValidationError: Falha na validação do resultado após {self.max_attempts} tentativas. "
            f"Último erro: {last_error_msg}"
        )

    @staticmethod
    def _check_metrics(output: AnalysisOutputSchema, expected: Dict[str, Any]) -> None:
        got = output.metrics.model_dump()
        wrong = {k: (got.get(k), v) for k, v in expected.items() if got.get(k) != v}
        if wrong:
            details = "; ".join(f"{k}: recebido {g!r}, esperado {e!r}" for k, (g, e) in wrong.items())
            raise MetricsMismatchError(
                "O campo metrics deve repetir exatamente os valores calculados pelas ferramentas "
                f"determinísticas ({json.dumps(expected)}). Divergências: {details}"
            )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_random_exponential(min=1, max=5),
        reraise=True
    )
    def _call_llm_with_retry(self, prompt: str) -> str:
        """Chamada resiliente ao cliente de LLM com retry via tenacity."""
        return self.llm_client(prompt)
