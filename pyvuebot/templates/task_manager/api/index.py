import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html

from .routes import tasks, telegram

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Task Manager API",
        version="1.0.0",
        description="API for managing tasks in the Telegram Mini App",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Initialize FastAPI
app = FastAPI(
    openapi_url="/api/openapi.json",
    docs_url=None,
    redoc_url=None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.openapi = custom_openapi

# Include routers
app.include_router(tasks.router)
app.include_router(telegram.router)


@app.get("/api/docs", include_in_schema=False)
async def get_swagger_documentation():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title="Task Manager API Documentation",
        swagger_favicon_url="/favicon.ico"
    )


@app.on_event("startup")
async def startup_event():
    """Initialize bot on startup."""
    if telegram.application:
        logger.info("Initializing Telegram bot...")
        try:
            await telegram.application.initialize()
            logger.info("Telegram bot initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Telegram bot: {e}")
    else:
        logger.warning("No Telegram bot application available to initialize")


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    from .db import supabase

    bot_status = "initialized" if telegram.application else "not initialized"
    db_status = "connected" if supabase else "not connected"

    return {
        "status": "healthy",
        "bot_status": bot_status,
        "database_status": db_status,
        "message": "API is running!"
    }


# @app.get("/{path:path}")
# async def serve_frontend(path: str):
#     import os

#     # Check if running in production (Vercel)
#     if os.environ.get("VERCEL", "0") == "1":
#         # Serve index.html for empty path
#         if not path or path == "":
#             return FileResponse("dist/index.html")

#         # Check if file exists in dist
#         file_path = f"dist/{path}"
#         if os.path.exists(file_path):
#             return FileResponse(file_path)

#         # Fallback to index.html for client-side routing
#         return FileResponse("dist/index.html")

#     # Development message
#     return {
#         "message": "API is running. Frontend is served separately in development."
#     }
