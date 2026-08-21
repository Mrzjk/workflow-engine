import structlog
def configure_logging() -> None:
    structlog.configure(processors=[structlog.contextvars.merge_contextvars, structlog.processors.JSONRenderer()])
