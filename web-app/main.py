import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/src")

from app import app   # noqa
from layout import app_layout   # noqa
from callback import upload_csv   # noqa


app.layout = app_layout

if __name__ == "__main__":
    DEBUG = bool(int(os.getenv("DEBUG", "0")))
    app.run_server(debug=DEBUG)
