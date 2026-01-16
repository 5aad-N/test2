from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

def health_check(request):
    logger.info(f"Health check request headers: {request.headers}")
    return HttpResponse("OK")
