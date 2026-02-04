from __future__ import annotations

from typing import List, Dict, Any

CHICKEN_LADDER: List[float] = [
    1.03, 1.07, 1.12, 1.17, 1.23,
    1.29, 1.36, 1.44, 1.53, 1.63,
    1.75, 1.88, 2.04, 2.22, 2.45,
    2.72, 3.06, 3.50, 4.08, 4.90,
    6.13, 6.61, 9.81, 19.44
]

# Usamos 2 casas porque a ladder tem 2 casas
_LADDER_INDEX = {round(v, 2): i for i, v in enumerate(CHICKEN_LADDER)}


def analyze_sequence(history: List[float]) -> Dict[str, Any]:
    """
    Regra:
    - precisa de pelo menos 3 valores
    - pega os últimos 3
    - todos devem estar na escada (comparando por round(.,2))
    - se os índices sobem (crescente), sinal BET com alvo = próximo nível
    """
    if not history or len(history) < 3:
        return {"signal": "NO_BET", "reason": "Histórico insuficiente"}

    last = history[-3:]

    # normaliza para 2 casas (evita problema de float)
    last_norm = [round(float(x), 2) for x in last]

    indices: List[int] = []
    for h in last_norm:
        idx = _LADDER_INDEX.get(h)
        if idx is None:
            return {"signal": "NO_BET", "reason": "Valor fora da escada real"}
        indices.append(idx)

    # sequência crescente
    if indices[0] < indices[1] < indices[2]:
        next_index = indices[2] + 1

        if next_index >= len(CHICKEN_LADDER):
            return {"signal": "NO_BET", "reason": "Topo da escada"}

        target = CHICKEN_LADDER[next_index]

        return {
            "signal": "BET",
            "target": target,
            "confidence": "REAL",
            "reason": (
                f"Escada crescente detectada: "
                f"{last_norm[0]}x → {last_norm[1]}x → {last_norm[2]}x"
            ),
        }

    return {"signal": "NO_BET", "reason": "Sem sequência crescente"}
