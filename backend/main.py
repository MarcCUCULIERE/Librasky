from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
from app.routes import whisky

app = FastAPI(
    title="Librasky API",
    description="""
    # 🥃 API de Gestion de Cave à Whisky

    ## Fonctionnalités

    Cette API permet de :
    * Gérer une collection de whiskies
    * Stocker des images de bouteilles
    * Importer/Exporter des données
    * Noter et commenter les whiskies

    ## Authentification
    *À implémenter dans une future version*

    ## Notes techniques
    * Les images sont stockées en base64 dans la base de données
    * Les données sont stockées dans une base SQLite
    * L'API suit les principes REST
    """,
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Support Librasky",
        "url": "http://example.com/contact/",
        "email": "contact@librasky.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "whiskies",
            "description": "Opérations liées à la gestion des whiskies",
            "externalDocs": {
                "description": "Guide d'utilisation",
                "url": "http://example.com/docs/whiskies/",
            },
        },
    ],
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(whisky.router)

# Route racine
@app.get("/",
    tags=["root"],
    summary="Page d'accueil",
    description="Retourne les informations de base de l'API")
def read_root():
    """
    Retourne un message de bienvenue et les liens vers la documentation
    """
    return {
        "message": "Bienvenue sur l'API Librasky",
        "documentation": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)