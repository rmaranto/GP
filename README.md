# App de Fila Virtual con SMS

Esta app permite:

1. Registrar clientes por número telefónico.
2. Asignar turno automáticamente.
3. Notificar por SMS cuando se registran y cuando les toca pasar.

## Tecnologías

- FastAPI
- API REST
- Integración SMS (stub listo para Twilio/Vonage/SNS)

## Ejecutar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

## Endpoints

### `POST /queue/join`
Registra un teléfono en la fila.

Ejemplo:

```json
{
  "phone": "+525511223344"
}
```

### `POST /queue/advance`
Avanza la fila y notifica por SMS a quien sigue.

Ejemplo:

```json
{
  "count": 1
}
```

### `GET /queue`
Consulta estado actual de la fila.

## Integrar SMS real

Reemplaza la función `send_sms` en `app.py` con el proveedor que uses:

- Twilio
- Vonage
- AWS SNS

Sugerencia: usa variables de entorno para credenciales (`SMS_API_KEY`, `SMS_SENDER_ID`, etc.).
