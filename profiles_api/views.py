from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from profiles_api import serializers


class HelloApiView(APIView):
    """Test api view"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returtn a list of apiview featurs"""
        an_apiview = [
            'Uses HTTP method as fucntion get,post,patch,put,delete',
            'is similar to a traditional Django view',
            'give you the most control over your app logic',
            'Is mapped manually to urls'
        ]

        return Response({'Message': 'Hello', 'an_apiview': an_apiview})

    def post(self, request):
        """Cresate a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk=None):
        """Handle updateing an object"""
        return Response({'mehtod': 'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """delete an object"""
        return Response({'mehtod': 'DELETE'})
