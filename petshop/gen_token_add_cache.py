import jwt
import inspect, os
from django.utils.deconstruct import deconstructible
from rest_framework.authentication import (
    get_authorization_header,
)

@deconstructible
class GenCacheKey:
    def __init__(self, request):
        payload_data = get_values_token(request)
        if payload_data is None:
            self.key_prefix = "Ftech_cache"
        else:
            self.key_prefix ='User_'+ str(payload_data['sub'])+"_"+request.path
    
def get_values_token(request):
    auth = get_authorization_header(request).split()
    try:
        token = auth[1]
    except:  
        return None     
    payload_data = jwt.decode(token, verify=False)
    return payload_data