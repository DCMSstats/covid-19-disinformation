import logging
from google.cloud import logging as cloudlogging

from google.cloud import error_reporting
_error_client = error_reporting.Client()


_log_client = cloudlogging.Client()
_log_handler = _log_client.get_default_handler()
cloud_logger = logging.getLogger("cloudLogger")
cloud_logger.setLevel(logging.INFO)
cloud_logger.addHandler(_log_handler)


def report_errors(func):
    """
    Decorator to report errors to GCP Error Reporting.
    For use on high level API function, to inform when.
    """
    def wrapper(*args, **kwargs):
        if "context" in kwargs:
            context = kwargs.get("context")
            cloud_logger.info(f"Triggered by messageId {context.event_id} published at {context.timestamp}")

        try:
            return func(*args, **kwargs)
        except Exception as e:
            cloud_logger.error(e)
            _error_client.report_exception()
    
    return wrapper
