from typing import List, Dict, Any

class DeterministicTools:
    """
    Ferramentas Python determinísticas para cálculos numéricos e estatísticos.
    Garante que a LLM não alucine operações aritméticas ou avaliações de risco.
    """

    @staticmethod
    def calculate_risk_score(items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calcula o risco e a pontuação total com base nos itens analisados.
        """
        if not items:
            return {
                "total_score": 100.0,
                "risk_level": "LOW",
                "calculated_items": 0
            }

        total_items = len(items)
        high_risk_count = sum(1 for item in items if item.get("severity") == "HIGH")
        medium_risk_count = sum(1 for item in items if item.get("severity") == "MEDIUM")

        # Fórmula determinística de score (0 a 100)
        deduction = (high_risk_count * 25.0) + (medium_risk_count * 10.0)
        score = max(0.0, 100.0 - deduction)

        if score < 50.0:
            risk_level = "HIGH"
        elif score < 80.0:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "total_score": round(score, 2),
            "risk_level": risk_level,
            "calculated_items": total_items
        }
