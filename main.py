from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Chicken Road Signal API")

ESCADA = [
    1.03, 1.07, 1.12, 1.17, 1.23, 1.29, 1.36, 1.44,
    1.53, 1.63, 1.75, 1.88, 2.04, 2.22, 2.45, 2.72,
    3.06, 3.50, 4.08, 4.90, 6.13, 6.61, 9.81, 19.44
]

class SignalRequest(BaseModel):
    history: list[float]

@app.post("/signal")
def signal(data: SignalRequest):
    history = data.history

    if len(history) < 5:
        return {
            "signal": "NO_BET",
            "reason": "Histórico insuficiente"
        }

    last = history[-1]

    # encontra posição atual na escada
    next_levels = [x for x in ESCADA if x > last]

    if not next_levels:
        return {
            "signal": "NO_BET",
            "reason": "Escada finalizada"
        }

    return {
        "signal": "BET",
        "current": f"{last:.2f}x",
        "next_levels": [f"{x:.2f}x" for x in next_levels],
        "reason": (
            f"Último multiplicador {last:.2f}x "
            "está dentro da escada estatística natural"
        )
    }
