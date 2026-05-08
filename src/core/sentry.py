import sentry_sdk
import structlog
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from src.schemas.config import log_settings

def before_send(event, hint):
    request = event.get("request")
    context = structlog.contextvars.get_contextvars()
    event.setdefault("extra", {})
    event["extra"]["request_id"] = context.get("request_id")
    
    if request and "headers" in request:
        request["headers"].pop("authorization", None)

    return event

def setup_sentry() -> None:
    if not log_settings.SENTRY_DSN:
        return

    sentry_sdk.init(
        dsn=log_settings.SENTRY_DSN,

        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
        ],
        before_send=before_send,
        traces_sample_rate=log_settings.SENTRY_TRACES_SAMPLE_RATE,

        profile_session_sample_rate=1.0,
        profile_lifecycle="trace",

        environment=log_settings.ENVIRONMENT,
    )
