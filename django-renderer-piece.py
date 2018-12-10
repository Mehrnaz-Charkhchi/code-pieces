from django.http import FileResponse
from rest_framework import viewsets, renderers
from rest_framework.decorators import action

class PassthroughRenderer(renderers.BaseRenderer):
    """
        Return data as-is. View should supply a Response.
    """
    media_type = ''
    format = ''
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

class ExampleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Example.objects.all()

    @action(methods=['get'], detail=True, renderer_classes=(PassthroughRenderer,))
    def download(self, *args, **kwargs):
        instance = self.get_object()

        # get an open file handle (I'm just using a file attached to the model for this example):
        file_handle = instance.file.open()

        # send file
        response = FileResponse(file_handle, content_type='whatever')
        response['Content-Length'] = instance.file.size
        response['Content-Disposition'] = 'attachment; filename="%s"' % instance.file.name

        return response
 #Inspiration for writing custom renderer classes=> Source: https://stackoverflow.com/questions/38697529/how-to-return-generated-file-download-with-django-rest-framework
