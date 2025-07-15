# Chat RAG + FastAPI + Next.js

Este proyecto combina un motor RAG (Retrieval-Augmented Generation) usando ChromaDB + OpenAI con un backend en FastAPI y una interfaz web en Next.js exportada como HTML estático. Toda la aplicación puede ejecutarse en local o contenerizarse fácilmente.

---

## Requisitos

- Python 3.11+
- Node.js 18+
- npm 9+ (o yarn)
- Docker (opcional, para entornos contenerizados)

---

## Instrucciones para correr el proyecto

### 1. Clona el repositorio

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
```

---

### 2. Configura el backend (FastAPI)

#### a. Instala dependencias

```bash
cd app
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### b. Ejecuta el backend

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

> Esto iniciará FastAPI sirviendo la API en `http://localhost:8000/api` y los archivos estáticos en `http://localhost:8000/static`

---

### 3. Prepara el frontend (Next.js)

#### a. Instala dependencias

```bash
cd frontend
npm install
```

#### b. Configura `next.config.ts` para exportar estático

```ts
const nextConfig = {
  output: "export",
  basePath: "/static",
  assetPrefix: "/static/",
};

export default nextConfig;
```

#### c. Genera el sitio exportado

```bash
npm run build
```

Esto creará una carpeta `out/` con todos los archivos HTML estáticos.

#### d. Copia al backend para servirlos

```bash
cp -r out/* ../app/static/
```

---

### 4. Prueba la aplicación en el navegador

Abre:

```
http://localhost:8000/static/
```

O directamente:

```
http://localhost:8000/
```

(Si tienes redirección `/ → /static/` configurada)

---

## 📤 Endpoint para cargar documentos

Puedes subir documentos `.pdf`, `.txt`, `.docx` a ChromaDB vía:

```bash
curl -X POST http://localhost:8000/api/ingest \
  -F "file=@/ruta/a/tu_documento.pdf"
```

Esto dividirá el contenido, generará embeddings y los almacenará en tu vector store.

---

## 💬 Endpoint para hacer preguntas con RAG

Consulta tu base de conocimiento con:

```
POST /api/query
Content-Type: application/json

{
  "question": "¿Qué dice el Acuerdo 123 de 2013 sobre cancelaciones?"
}
```

Recibirás una respuesta generada a partir del contenido previamente indexado.

---

## 📂 Estructura del proyecto

```
├── app/                  # Backend FastAPI
│   ├── src/
│   │   ├── controllers/
│   │   ├── core/
│   │   ├── models/
│   │   ├── dto/
│   │   └── main.py
│   └── static/           # Frontend generado (Next.js exportado)
│
└── frontend/             # Código fuente Next.js (interfaz del chatbot)
```

---

## 🛠️ TODOs futuros

- [ ] Agregar autenticación JWT para el backend
- [ ] Soporte para múltiples colecciones en ChromaDB
- [ ] Descarga o exportación de respuestas como JSON o CSV
- [ ] Interfaz para cargar documentos desde el frontend

---

## 📃 Licencia

Este proyecto se encuentra bajo licencia MIT. Siéntete libre de usarlo, modificarlo y adaptarlo para tus necesidades.
