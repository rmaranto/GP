from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Fila Virtual SMS")


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


def send_sms(phone: str, message: str) -> None:
    """
    Integración SMS:
    Reemplaza esta función con Twilio/Vonage/AWS SNS.
    """
    print(f"[SMS] {phone}: {message}")


@app.post("/queue/join", response_model=QueueEntry)
def join_queue(payload: JoinQueueRequest):
    global next_ticket

    ticket = next_ticket
    next_ticket += 1

    entry = QueueEntry(
        ticket=ticket,
        phone=payload.phone,
        joined_at=datetime.utcnow(),
        status="waiting",
    )
    queue.append(entry)

    send_sms(payload.phone, f"Te registraste en la fila virtual. Tu turno es #{ticket}.")

    return entry


@app.post("/queue/advance", response_model=QueueState)
def advance_queue(payload: AdvanceQueueRequest):
    global now_serving

    for _ in range(payload.count):
        waiting = [e for e in queue if e.status == "waiting"]
        if not waiting:
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

    waiting_entries = [e for e in queue if e.status == "waiting"]
    return QueueState(waiting=waiting_entries, now_serving=now_serving)


@app.get("/queue", response_model=QueueState)
def get_queue_state():
    waiting_entries = [e for e in queue if e.status == "waiting"]
    return QueueState(waiting=waiting_entries, now_serving=now_serving)
