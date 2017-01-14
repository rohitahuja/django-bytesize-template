import hashlib
import hmac
import json
import os

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .utils.handler import handle_payload


@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        header = request.META.get('HTTP_X_HUB_SIGNATURE', None)
        if not header:
            return HttpResponse("failed")

        sha_name, signature = header.split('=')
        if sha_name != 'sha1':
            return HttpResponse("failed")

        mac = hmac.new(os.environ.get('APP_SECRET'), msg=request.body, digestmod=hashlib.sha1)
        result = hmac.compare_digest(mac.hexdigest(), signature)
        if not result:
            return HttpResponse("failed")

        data = json.loads(request.body)
        handle_payload(payload=data)
        return HttpResponse("lol")
    else:
        if "hub.verify_token" in request.GET:
            if request.GET["hub.verify_token"] == "yeezyyeezywhatsgood":
                return HttpResponse(request.GET["hub.challenge"])
        return HttpResponse("You're not supposed to be here!")
