from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        print(kwargs)
        snippet = self.get_object()
        return Response(snippet.highlighted)

    @action(detail=False)
    def ruby(self, request, *args, **kwargs):
        ruby_snippets = self.get_queryset().filter(language="ruby")
        serializer = self.get_serializer(ruby_snippets, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def python(self, request, *args, **kwargs):
        python_snippets = self.get_queryset().filter(language="python")
        serializer = self.get_serializer(python_snippets, many=True)
        return Response(serializer.data)

    @action(detail=False, serializer_class= SnippetSerializer)
    def last_python(self, request, *args, **kwargs):
        last_python_snippet = self.get_queryset().filter(language="python").last()
        serializer = self.get_serializer(last_python_snippet)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
