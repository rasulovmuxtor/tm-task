from rest_framework.renderers import JSONRenderer


class ResultsJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = {'results': data}
        return super().render(data, accepted_media_type, renderer_context)
