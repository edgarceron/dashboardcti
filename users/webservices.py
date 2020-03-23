from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework import status

@api_view(['POST'])
def add_user(request):
    user_serializer = UserSerializer(data = request.data)
    if(user_serializer.is_valid()):
        user_serializer.save()
        return Response({"data":"Usuario guardado"}, status=status.HTTP_201_CREATED)
    else:
        error_details = []
        for key in user_serializer.errors.keys():
            error_details.append({"field": key, "message": user_serializer.errors[key][0]})

        data = {
            "Error": {
                "status": 400,
                "message": "Los datos enviados no son validos",
                "error_details": error_details
            }
        }

        return Response(data, status=status.HTTP_400_BAD_REQUEST)
