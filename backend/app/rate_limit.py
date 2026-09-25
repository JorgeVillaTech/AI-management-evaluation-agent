import time
from collections import defaultdict
from fastapi import Request, HTTPException

_requests: dict[str, list[float]] = defaultdict(list)
LIMIT = 10           # peticiones permitidas
WINDOW_SECONDS = 60  # por cada minuto

async def rate_limit(request: Request):
    ip = request.client.host
    now = time.time()
    ventana_inicio = now - WINDOW_SECONDS

    _requests[ip] = [t for t in _requests[ip] if t > ventana_inicio]

    if len(_requests[ip]) >= LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Demasiadas solicitudes. Intenta de nuevo en un minuto.",
        )

    _requests[ip].append(now)