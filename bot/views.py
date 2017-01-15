import json

from django.http import (
    HttpResponse,
    HttpResponseForbidden,
)
from django.views.decorators.csrf import csrf_exempt

from .utils.verify import (
    verify_request,
    verify_token,
)
from .utils.handle import handle_payload


@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        # Verify that the request is from Facebook
        if not verify_request(request):
            return HttpResponseForbidden("Request couldn't be verified.")

        # Handle the message payload
        data = json.loads(request.body)
        handle_payload(payload=data)

        # Notify success
        return HttpResponse("Request successful.")
    else:
        # Connecting webhook, must verify token
        response = verify_token(request)
        if response:
            return HttpResponse(response)

        # Otherwise, user not allowed here
        return HttpResponseForbidden("You're not supposed to be here!")
