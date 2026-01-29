import numpy as np

LEVELS = [
    1.03, 1.07, 1.12, 1.17, 1.23,
    1.29, 1.36, 1.44, 1.53, 1.63,
    1.75, 1.88, 2.04, 2.22, 2.45,
    2.72, 3.06, 3.50, 4.08, 4.90,
    6.13, 6.61, 9.81, 19.44
]

# 🧠 memória simples (runtime)
LAST_SIGNAL_INDEX = -1
COOLDOWN_ROUNDS = 3

def analyze_sequence(history: list[float]) -> dict:
    global LAST_SIGNAL_INDEX

    if len(history) < 12:
        return {
            "signal": "NO_BET",
            "reason": "Histórico insuficiente"
        }

    current_index = len(history)

    # ⏳ Cooldown
    if LAST_SIGNAL_INDEX != -1:
        if current_index - LAST_SIGNAL_INDEX <= COOLDOWN_ROUNDS:
            return {
                "signal": "NO_BET",
                "reason": "Cooldown ativo – aguardando novas rodadas"
            }

    last = history[-1]
    recent = history[-6:]

    slope = np.polyfit(range(len(recent)), recent, 1)[0]
    volatility = np.std(recent)

    target = None
    for lvl in LEVELS:
        if lvl > last:
            target = lvl
            break

    if not target:
        return {
            "signal": "NO_BET",
            "reason": "Topo da escada atingido"
        }

    if slope < -0.05:
        return {
            "signal": "NO_BET",
            "reason": "Tendência negativa"
        }

    if volatility > 1.2:
        return {
            "signal": "NO_BET",
            "reason": "Volatilidade alta"
        }

    # 🟢 sinal aprovado
    LAST_SIGNAL_INDEX = current_index

    return {
        "signal": "BET",
        "target": target,
        "confidence": "ALTA" if volatility < 0.6 else "MÉDIA",
        "reason": (
            f"Tendência favorável\n"
            f"Volatilidade controlada ({volatility:.2f})\n"
            f"Próximo nível real: {target}x"
        )
    }
