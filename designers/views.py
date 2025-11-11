from rest_framework import viewsets, permissions
from .models import Package, DesignerProfile
from .serializers import PackageSerializer, DesignerProfileSerializer

class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Package.objects.all().order_by('price_cents')
    serializer_class = PackageSerializer
    permission_classes = [permissions.AllowAny]

class DesignerProfileViewSet(viewsets.ModelViewSet):
    queryset = DesignerProfile.objects.all()
    serializer_class = DesignerProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Link designer profile to the logged-in user
        serializer.save(user=self.request.user)
