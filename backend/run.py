import os

from app import create_app

app = create_app()  # construye la aplicación Flask con configuración, blueprints y base de datos

if __name__ == "__main__":
    # Escucha en todas las interfaces para que el contenedor Docker pueda redirigir el puerto
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)