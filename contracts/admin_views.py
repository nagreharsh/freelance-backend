from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from common.permissions import IsAdminRole
from .models import Contract
from .serializers import ContractSerializer


class AdminContractViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Contract.objects.all().order_by("-created_at")
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]