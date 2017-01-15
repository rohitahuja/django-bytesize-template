import hashlib
import hmac
import os


def verify_request(request):
    """verify_request

    Verifies that the given request is from Facebook
    """
    header = request.META.get('HTTP_X_HUB_SIGNATURE', None)
    if not header:
        return False

    sha_name, signature = header.split('=')
    if sha_name != 'sha1':
        return False

    mac = hmac.new(os.environ.get('APP_SECRET'), msg=request.body, digestmod=hashlib.sha1)
    result = hmac.compare_digest(mac.hexdigest(), signature)

    return result


def verify_token(request):
    """verify_token

    Verifies token during webhook setup
    """
    if "hub.verify_token" in request.GET:
        token = os.environ.get('VERIFY_TOKEN', "yeezyyeezywhatsgood")
        if request.GET["hub.verify_token"] == token:
            return request.GET["hub.challenge"]

    return None
