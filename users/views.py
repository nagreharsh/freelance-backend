import logging
logger = logging.getLogger(__name__)

from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework import status
from common.throttles import LoginRateThrottle

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        logger.info(
            f"User registered username={user.username} role={user.role}"
        )

        return Response(
            {'message': 'Registration successful. Please log in.'},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@throttle_classes([LoginRateThrottle])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        logger.info(
            f"User login username={user.username}"
        )

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'role': user.role,
            'username': user.username,
        })

    return Response(
        {'detail': 'Invalid username or password. Please try again.'},
        status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            logger.info(
                f"Profile updated username={request.user.username}"
            )

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Admin Views

from .models import User

def is_admin(user):
    return user.role == 'admin' or user.is_staff

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_list_unverified_users(request):
    if not is_admin(request.user):
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    unverified_profiles = Profile.objects.filter(is_verified=False)
    users = [p.user for p in unverified_profiles]
    
    data = []
    for user in users:
        data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'profile_filled': bool(user.profile.bio and user.profile.skills)
        })
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_verify_user(request, user_id):
    if not is_admin(request.user):
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        user = User.objects.get(pk=user_id)
        profile = user.profile
        profile.is_verified = True
        profile.save()

        logger.info(
            f"Admin {request.user.username} verified user {user.username}"
        )

        return Response({'status': 'User verified successfully'})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Profile.DoesNotExist:
         return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_demand_stats(request):
    if not is_admin(request.user):
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    threshold = int(request.query_params.get('threshold', 5))
    
    high_demand = Profile.objects.filter(user__role='client', proposals_received_count__gte=threshold)
    low_demand = Profile.objects.filter(user__role='client', proposals_received_count=0)
    
    high_data = [{'username': p.user.username, 'proposals_count': p.proposals_received_count} for p in high_demand]
    low_data = [{'username': p.user.username, 'proposals_count': p.proposals_received_count} for p in low_demand]
    
    return Response({
        'high_demand_clients': high_data,
        'low_demand_clients': low_data
    })


'''
This is to see every registered users in the backend, require admin authentication token
'''
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import User

@api_view(["GET"])
@permission_classes([IsAdminUser])
def list_users(request):
    users = User.objects.all().values("id", "username", "role")
    return Response(users)