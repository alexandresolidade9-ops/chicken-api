CHICKEN_LADDER = [
    1.03, 1.07, 1.12, 1.17, 1.23,
    1.29, 1.36, 1.44, 1.53, 1.63,
    1.75, 1.88, 2.04, 2.22, 2.45,
    2.72, 3.06, 3.50, 4.08, 4.90,
    6.13, 6.61, 9.81, 19.44
]

def analyze_sequence(history):
    if len(history) < 3:
        return {
            "signal": "NO_BET",
            "reason": "Histórico insuficiente"
        }

    # pega últimos 3
    last = history[-3:]

    # verifica se estão na escada
    indices = []
    for h in last:
        if h not in CHICKEN_LADDER:
            return {
                "signal": "NO_BET",
                "reason": "Valor fora da escada real"
            }
        indices.append(CHICKEN_LADDER.index(h))

    # verifica subida
    if indices[0] < indices[1] < indices[2]:
        next_index = indices[-1] + 1

        if next_index >= len(CHICKEN_LADDER):
            return {
                "signal": "NO_BET",
                "reason": "Topo da escada"
            }

        target = CHICKEN_LADDER[next_index]

        return {
            "signal": "BET",
            "target": target,
            "confidence": "REAL",
            "reason": (
                f"Escada crescente detectada: "
                f"{last[0]}x → {last[1]}x → {last[2]}x"
            )
        }

    return {
        "signal": "NO_BET",
        "reason": "Sem sequência crescente"
    }
