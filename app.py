from datetime import datetime, timezone
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Fila Virtual SMS", version="1.1.0")


class JoinQueueRequest(BaseModel):
    phone: str = Field(..., min_length=10, max_length=20, description="Número telefónico del cliente")


class AdvanceQueueRequest(BaseModel):
    count: int = Field(1, ge=1, le=50)


class QueueEntry(BaseModel):
    ticket: int
    phone: str
    joined_at: datetime
    status: str


class QueueState(BaseModel):
    waiting: List[QueueEntry]
    now_serving: Optional[int]


queue: List[QueueEntry] = []
now_serving: Optional[int] = None
next_ticket = 1


def reset_state() -> None:
    global queue, now_serving, next_ticket
    queue = []
    now_serving = None
    next_ticket = 1


def send_sms(phone: str, message: str) -> None:
    """Integración SMS placeholder para reemplazar con proveedor real."""
    print(f"[SMS] {phone}: {message}")


def waiting_entries() -> List[QueueEntry]:
    return [e for e in queue if e.status == "waiting"]


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/queue/join", response_model=QueueEntry)
def join_queue(payload: JoinQueueRequest):
    global next_ticket

    if any(e.phone == payload.phone and e.status == "waiting" for e in queue):
        raise HTTPException(status_code=409, detail="Este número ya está en espera.")

    ticket = next_ticket
    next_ticket += 1

    entry = QueueEntry(
        ticket=ticket,
        phone=payload.phone,
        joined_at=datetime.now(timezone.utc),
        status="waiting",
    )
    queue.append(entry)

    send_sms(payload.phone, f"Te registraste en la fila virtual. Tu turno es #{ticket}.")
    return entry


@app.post("/queue/advance", response_model=QueueState)
def advance_queue(payload: AdvanceQueueRequest):
    global now_serving

    for _ in range(payload.count):
        # Cerrar turno anterior en servicio
        if now_serving is not None:
            for idx, entry in enumerate(queue):
                if entry.ticket == now_serving and queue[idx].status == "serving":
                    queue[idx].status = "done"
                    break

        waiting = waiting_entries()
        if not waiting:
            now_serving = None
            break

        current = waiting[0]
        for idx, entry in enumerate(queue):
            if entry.ticket == current.ticket:
                queue[idx].status = "serving"
                now_serving = current.ticket
                send_sms(
                    queue[idx].phone,
                    f"¡Es tu turno! Pasa a caja ahora. Turno #{queue[idx].ticket}.",
                )
                break

    return QueueState(waiting=waiting_entries(), now_serving=now_serving)


@app.get("/queue", response_model=QueueState)
def get_queue_state():
    return QueueState(waiting=waiting_entries(), now_serving=now_serving)
