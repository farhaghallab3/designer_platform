from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order, OrderFile
from .serializers import OrderSerializer, OrderFileSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(client=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated], parser_classes=[MultiPartParser, FormParser])
    def upload_file(self, request, pk=None):
        order = self.get_object()
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'detail':'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        of = OrderFile.objects.create(order=order, file=file_obj)
        return Response(OrderFileSerializer(of).data, status=status.HTTP_201_CREATED)
