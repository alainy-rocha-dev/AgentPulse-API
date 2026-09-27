import json
import logging
import time
from typing import Callable, Any
from pydantic import ValidationError
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type

from app.schemas.agent_output import AnalysisOutputSchema

logger = logging.getLogger(__name__)

class SchemaValidationError(Exception):
    """Exceção customizada quando o Repair Loop atinge o limite de tentativas."""
    pass

class RepairLoopService:
    """
    Serviço de Repair Loop Anti-Alucinação.
    Executa re-prompting com o erro do Pydantic se o LLM gerar um JSON malformado.
    """

    def __init__(self, llm_client: Callable[[str], str], max_attempts: int = 3):
        self.llm_client = llm_client
        self.max_attempts = max_attempts

    def execute_with_repair(self, initial_prompt: str) -> AnalysisOutputSchema:
        current_prompt = initial_prompt
        last_error_msg = ""
        start_time = time.time()

        for attempt in range(1, self.max_attempts + 1):
            logger.info(f"Executando tentativa {attempt} de {self.max_attempts} no Repair Loop.")
            try:
                raw_response = self._call_llm_with_retry(current_prompt)
                
                # Tentar parsing de JSON e validação via Pydantic
                json_data = json.loads(raw_response)
                validated_output = AnalysisOutputSchema(**json_data)
                
                # Atualizar metadados
                elapsed_time = round(time.time() - start_time, 2)
                validated_output.metadata.repair_attempts = attempt - 1
                validated_output.metadata.execution_time_seconds = elapsed_time

                logger.info(f"Resultado validado com sucesso na tentativa {attempt}.")
                return validated_output

            except (json.JSONDecodeError, ValidationError) as exc:
                last_error_msg = str(exc)
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

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_random_exponential(min=1, max=5),
        reraise=True
    )
    def _call_llm_with_retry(self, prompt: str) -> str:
        """Chamada resiliente ao cliente de LLM com retry via tenacity."""
        return self.llm_client(prompt)
