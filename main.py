"""
Punto de entrada principal de PerfumeShop AI.

Este archivo inicia el servidor FastAPI con todos los componentes.
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


def main():
    """
    Inicia el servidor FastAPI.
    Comando para ejecutar:
    python main.py

    O directamente con uvicorn:
    uvicorn api.endpoints:app --reload
    """
    import uvicorn

    # Obtener configuración desde variables de entorno
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))

    # Verificar que ANTHROPIC_API_KEY esté configurada
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  ADVERTENCIA: ANTHROPIC_API_KEY no está configurada")
        print("   Configura tu API key en el archivo .env")
        return

    print("🚀 Iniciando PerfumeShop AI API...")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Docs: http://{host}:{port}/docs")

    # Iniciar servidor
    uvicorn.run(
        "api.endpoints:app",
        host=host,
        port=port,
        reload=True  # Auto-reload en desarrollo
    )


if __name__ == "__main__":
    main()
