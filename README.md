# App de Fila Virtual con SMS

Esta app permite:

1. Registrar clientes por número telefónico.
2. Asignar turno automáticamente.
3. Notificar por SMS cuando se registran y cuando les toca pasar.

## Tecnologías

- FastAPI
- API REST
- Integración SMS (stub listo para Twilio/Vonage/SNS)

## Ejecutar local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Abrir desde otra PC (misma red)

1. Obtén la IP local de la PC donde corre la app:

```bash
hostname -I
```

2. Desde la otra PC, abre en navegador:

```text
http://TU_IP_LOCAL:8000/docs
```

Ejemplo: `http://192.168.1.50:8000/docs`

> Si no abre, revisa firewall y que ambas PCs estén en la misma red.

## Publicarla en internet (rápido con Render)

1. Sube este proyecto a GitHub.
2. En https://render.com crea un **Web Service** desde tu repo.
3. Configura:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. Deploy.
5. Render te dará una URL pública como:
   - `https://tu-app.onrender.com/docs`

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
