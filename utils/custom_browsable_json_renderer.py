from rest_framework.renderers import BrowsableAPIRenderer
from .custom_json_renderer import CustomJSONRenderer

class CustomBrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_default_renderer(self, view):
        return CustomJSONRenderer()
