from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import RegisterSerializer


#unverified users
class UnverifiedUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "admin":
            return Response({"error": "Admin only"}, status=403)

        users = User.objects.filter(is_verified=False)
        serializer = RegisterSerializer(users, many=True)
        return Response(serializer.data)

#Verify user
class VerifyUserView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, user_id):
        if request.user.role != "admin":
            return Response({"error": "Admin only"}, status=403)

        user = User.objects.get(id=user_id)
        user.is_verified = True
        user.save()

        return Response({"message": "User verified"})
