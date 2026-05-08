import time
import uuid

import structlog
from fastapi import Request
from starlette.responses import Response

logger = structlog.get_logger()


async def logging_middleware(
    request: Request,
    call_next,
) -> Response:

    request_id = str(uuid.uuid4())

    request.state.request_id = request_id

    client_ip = request.client.host if request.client else None

    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        path=request.url.path,
        method=request.method,
        client_ip=client_ip,
    )

    start_time = time.perf_counter()

    logger.info(
        "request_started",
    )

    try:
        response = await call_next(request)

    except Exception:
        logger.exception("unhandled_exception")
        raise

    process_time = round(
        time.perf_counter() - start_time,
        4,
    )

    logger.info(
        "request_finished",
        status_code=response.status_code,
        process_time=process_time,
    )

    response.headers["X-Request-ID"] = request_id

    structlog.contextvars.clear_contextvars()

    return response