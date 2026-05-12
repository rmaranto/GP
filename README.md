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


## Publicación definitiva (producción)

Este repo ya incluye despliegue listo para Render y Docker:

- `render.yaml` para despliegue automático en Render.
- `Dockerfile` para ejecutar en cualquier VPS/container.

### Opción A: Render (recomendada)

1. Sube este repositorio a GitHub.
2. En Render selecciona **New + > Blueprint**.
3. Conecta tu repo y confirma el deploy.
4. Render leerá `render.yaml` y publicará automáticamente.
5. URL final: `https://<tu-servicio>.onrender.com/docs`

### Opción B: Docker en VPS

```bash
docker build -t fila-virtual-sms .
docker run -d --name fila-virtual-sms -p 80:10000 fila-virtual-sms
```

URL final: `http://IP_PUBLICA/docs`

### Checklist para que sí abra públicamente

- Abrir puerto 80 o 443 en firewall/security group.
- Mantener el servicio escuchando en `0.0.0.0`.
- Si usas dominio, apuntar DNS a tu IP o URL de Render.
