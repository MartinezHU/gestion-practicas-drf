import json
import logging
import sys
from datetime import datetime
from functools import wraps

class _APILoggerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger = logging.getLogger("api")
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler(sys.stdout)
            logger.addHandler(handler)
            logger.propagate = False
            cls._instance = logger
        return cls._instance

logger = _APILoggerSingleton()


class APILogger:
    @staticmethod
    def get_request_data(request):
        return {
            "m": request.method,
            "p": request.path,
            "u": str(request.user.id) if request.user.is_authenticated else None,
            "ip": request.META.get("REMOTE_ADDR"),
        }

    @staticmethod
    def log(message, request=None, extra=None, level="info"):
        data = {"t": datetime.now().isoformat(), "msg": message}
        if request:
            data.update(APILogger.get_request_data(request))
        if isinstance(extra, dict):
            data.update(extra)

        getattr(logger, level)(json.dumps(data))


def log_api_call(level="info"):
    def decorator(func):
        @wraps(func)
        def wrapper(view, request, *a, **kw):
            APILogger.log(f"▶ {view.__class__.__name__}.{func.__name__}", request, {"e": 1}, level=level)
            try:
                r = func(view, request, *a, **kw)
                if hasattr(r, "status_code"):
                    APILogger.log(f"✓ {view.__class__.__name__}.{func.__name__}", request, {"s": r.status_code}, level=level)
                return r
            except Exception as e:
                APILogger.log(f"✖ {view.__class__.__name__}.{func.__name__}", request, {"err": str(e)}, level="error")
                raise
        return wrapper
    return decorator

def log_all_api_calls(level="info"):
    def class_decorator(cls):
        for attr_name in dir(cls):
            if attr_name in ("list", "retrieve", "create", "update", "partial_update", "destroy"):
                method = getattr(cls, attr_name, None)
                if callable(method):
                    decorated = log_api_call(level)(method)
                    setattr(cls, attr_name, decorated)
        return cls
    return class_decorator
