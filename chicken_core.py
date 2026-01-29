import numpy as np

TARGET_LEVELS = [2, 3, 5, 10, 20]

def analyze_sequence(history):
    MIN_HISTORY = 12

    if len(history) < MIN_HISTORY:
        return {
            "signal": "NO_BET",
            "reason": "Histórico insuficiente"
        }

    recent = np.array(history[-MIN_HISTORY:])
    diffs = np.diff(recent)

    # crescimento consistente
    growth_ratio = np.mean(diffs > 0)
    avg_growth = np.mean(diffs)

    if growth_ratio < 0.65:
        return {
            "signal": "NO_BET",
            "reason": "Crescimento inconsistente"
        }

    last = recent[-1]

    # evitar entrada esticada demais
    if last > 3.0:
        return {
            "signal": "NO_BET",
            "reason": "Sequência já esticada"
        }

    # detectar aceleração
    accel = np.mean(diffs[-5:]) - np.mean(diffs[:5])

    if accel <= 0:
        return {
            "signal": "NO_BET",
            "reason": "Sem aceleração clara"
        }

    # escolher alvo realista
    target = None
    for lvl in TARGET_LEVELS:
        if lvl > last:
            target = lvl
            break

    confidence = "ALTA" if accel > 0.15 else "MÉDIA"

    return {
        "signal": "BET",
        "target": f"{target}x",
        "confidence": confidence,
        "reason": (
            f"Sequência crescente com aceleração "
            f"(último={last:.2f}x, aceleração={accel:.2f})"
        )
    }
