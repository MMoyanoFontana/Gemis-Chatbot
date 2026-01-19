# Gemis Chatbot

Chatbot avanzado para **Retrieval Augmented Generation (RAG)**, diseñado para responder preguntas sobre documentos PDF cargados por el usuario. Desarrollado para el grupo **GEMIS.BA**.

Utiliza **LangChain** y **LangGraph** para la orquestación, y **Gradio** para la interfaz de usuario.

> **Objetivo:** Permitir la carga de documentos, indexación semántica y consultas en lenguaje natural con persistencia de sesiones.

---

## Características

- **Carga y procesamiento de PDFs** con `PyMuPDF`.
- **Búsqueda semántica** utilizando ChromaDB (o vector store configurado).
- **Orquestación inteligente** con LangGraph.
- **Persistencia de chats y archivos** en SQLite.
- **Autenticación simple** de usuarios.
- **Interfaz moderna** y responsiva con Gradio.

## Requisitos Previos

- Python 3.12 o superior.
- [uv](https://github.com/astral-sh/uv) (Recomendado) o `pip`.
- API Key de OpenAI (u otro proveedor configurado).

## Instalación

### Opción A: Usando uv (Recomendado)

```bash
git clone https://github.com/MMoyanoFontana/Gemis-Chatbot
cd Gemis-Chatbot
uv sync
```

### Opción B: Usando pip

```bash
git clone https://github.com/MMoyanoFontana/Gemis-Chatbot
cd Gemis-Chatbot
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

1. **Variables de Entorno**:
   Crea un archivo `.env` en la raíz o exporta las variables directamente:
   ```bash
   OPENAI_API_KEY=sk-... # o la API key de otro proveedor
   # Opcional: para trazabilidad con LangSmith
   LANGSMITH_API_KEY=...
   LANGSMITH_TRACING=true
   ```

2. **Configuración de Modelos (`config.yaml`)**:
   Asegúrate de que `config.yaml` tenga los modelos correctos:
   ```yaml
   EMBED_MODEL: "openai:text-embedding-3-large"
   CHAT_MODEL: "openai:gpt-4o-mini"
   # ... otras configuraciones
   ```

## Ejecución

Para iniciar la aplicación:

```bash
# Con uv
uv run python src/main.py

# O con python directo (si se usa pip)
python src/main.py
```

La aplicación estará disponible en `http://localhost:7860` (o la URL que indique la consola).

## Uso

1. **Iniciar Sesión**: Usa el usuario creado desde la CLI (ver base de datos) o crea uno nuevo usando `src/db.py`.
2. **Nuevo Chat**: Crea un hilo de conversación.
3. **Subir Archivo**: Carga un PDF. El sistema lo procesará e indexará.
4. **Preguntar**: Interactúa con el chatbot sobre el contenido del documento.

## Gestión de Usuarios (CLI)

El archivo `src/db.py` incluye herramientas para gestionar la base de datos:

```bash
# Inicializar base de datos
uv run python src/db.py init

# Crear un usuario nuevo
uv run python src/db.py add <nombre_usuario>

# Listar usuarios
uv run python src/db.py list
```

## Estructura del Proyecto

- `src/main.py`: Punto de entrada de la aplicación Gradio.
- `src/graph.py`: Definición del grafo de LangGraph y RAG.
- `src/db.py`: Capa de persistencia (SQLite).
- `src/auth.py`: Utilidades de autenticación.
- `src/style.py`: Definiciones de estilos CSS y tema.
