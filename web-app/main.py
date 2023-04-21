import os
from app import app
from layout import app_layout

app.layout = app_layout

if __name__ == "__main__":
    DEBUG = bool(int(os.getenv("DEBUG", "0")))
    app.run_server(debug=DEBUG)
