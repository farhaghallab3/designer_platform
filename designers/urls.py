# designers/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PackageViewSet, 
    DesignerProfileViewSet,
    designers_list, 
    my_designer_profile, 
    create_designer_profile,
    test_view
)

router = DefaultRouter()
router.register(r'packages', PackageViewSet)
router.register(r'designer-profiles', DesignerProfileViewSet, basename='designerprofile')

urlpatterns = [
    path('', include(router.urls)),
    # Simple endpoints that will work
    path('all-designers/', designers_list, name='all-designers'),
    path('my-profile/', my_designer_profile, name='my-designer-profile'),
    path('create-profile/', create_designer_profile, name='create-designer-profile'),
    path('test/', test_view, name='test-view'),
]