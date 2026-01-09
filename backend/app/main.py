from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router as api_router
from fastapi.staticfiles import StaticFiles

def create_app() -> FastAPI:
    app = FastAPI(title="Research Assistant Backend", version="0.1.0")

    # -------------------------------------------------------------
    # 🔓 CORS CONFIGURATION
    # -------------------------------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",        # React local dev      # Alt localhost
             # (add production domain later)
        ],
        allow_credentials=True,
        allow_methods=["*"],   # allow GET, POST, PUT, DELETE, etc.
        allow_headers=["*"],   # allow all custom headers
        expose_headers=["Content-Disposition"],  # important for file downloads
    )
        # --- Serve generated files ---
    app.mount("/exports", StaticFiles(directory="exports"), name="exports")


    # -------------------------------------------------------------
    # Include API routes
    # -------------------------------------------------------------
    app.include_router(api_router)

    return app

app = create_app()