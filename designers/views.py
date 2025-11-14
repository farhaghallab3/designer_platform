# designers/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Package, DesignerProfile
from .serializers import PackageSerializer, DesignerProfileSerializer

User = get_user_model()

# Package ViewSet
class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Package.objects.all().order_by('price_cents')
    serializer_class = PackageSerializer
    permission_classes = [permissions.AllowAny]

# Designer Profile ViewSet
# class DesignerProfileViewSet(viewsets.ModelViewSet):
    queryset = DesignerProfile.objects.all()
    serializer_class = DesignerProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Simple function-based views for easier access
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def designers_list(request):
    """
    Get all designers with their profiles - PUBLIC endpoint
    """
    try:
        designer_profiles = DesignerProfile.objects.all()
        
        if not designer_profiles.exists():
            return Response([], status=status.HTTP_200_OK)
        
        serializer = DesignerProfileSerializer(designer_profiles, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_designer_profile(request):
    """Get current user's designer profile"""
    try:
        profile = DesignerProfile.objects.get(user=request.user)
        serializer = DesignerProfileSerializer(profile)
        return Response(serializer.data)
    except DesignerProfile.DoesNotExist:
        return Response(
            {"detail": "Designer profile not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_designer_profile(request):
    """Create designer profile for current user"""
    try:
        DesignerProfile.objects.get(user=request.user)
        return Response(
            {"detail": "Designer profile already exists"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except DesignerProfile.DoesNotExist:
        profile = DesignerProfile.objects.create(user=request.user, portfolio=[])
        serializer = DesignerProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def test_view(request):
    """Test if the view is working"""
    return Response({"message": "Designers app is working!", "status": "OK"})    

# designers/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class DesignerProfileViewSet(viewsets.ModelViewSet):
    queryset = DesignerProfile.objects.all()
    serializer_class = DesignerProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current user's designer profile"""
        try:
            profile = DesignerProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except DesignerProfile.DoesNotExist:
            return Response(
                {"detail": "Designer profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def create_my_profile(self, request):
        """Create designer profile for current user"""
        try:
            DesignerProfile.objects.get(user=request.user)
            return Response(
                {"detail": "Designer profile already exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except DesignerProfile.DoesNotExist:
            profile = DesignerProfile.objects.create(
                user=request.user, 
                portfolio=[], 
                rating=None
            )
            serializer = self.get_serializer(profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'])
    def update_portfolio(self, request, pk=None):
        """Update portfolio for specific designer profile"""
        profile = self.get_object()
        portfolio = request.data.get('portfolio', [])
        profile.portfolio = portfolio
        profile.save()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)