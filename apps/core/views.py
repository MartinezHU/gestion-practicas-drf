from rest_framework import viewsets

from apps.core.models import APIUser
from apps.core.serializers import APIUserSerializer
from main.logging import log_api_call, log_all_api_calls, logger


class LoggedViewSet(viewsets.ModelViewSet):
    def dispatch(self, request, *args, **kwargs):
        logger.info(f"Dispatch: {self.__class__.__name__}.{request.method}")
        return super().dispatch(request, *args, **kwargs)


class APIUserViewSet(LoggedViewSet):
    serializer_class = APIUserSerializer
    queryset = APIUser.objects.all()
