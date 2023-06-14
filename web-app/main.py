import argparse
import logging
import os
import sys
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/src")

from app import app   # noqa
from layout import app_layout   # noqa
from callback import upload_csv   # noqa


app.layout = app_layout

sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[
        sentry_logging,
    ],
    traces_sample_rate=1.0,
)


def argument_parser() -> bool:
    parser = argparse.ArgumentParser(description='Initiate the bot [-h HELP] [-t TOKEN] [-m MANUAL] [-l LOCAL].')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='start the server in debug mode, false by default')
    args = parser.parse_args()
    debug = args.debug
    return debug


if __name__ == "__main__":

    debug = True if argument_parser() else bool(int(os.getenv("DEBUG", "0")))
    app.run_server(host='0.0.0.0', port=8050, debug=debug)
