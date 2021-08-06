from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, SectorViewSet

app_name = "stock_api"

router = DefaultRouter()
router.register(r'sector', SectorViewSet, basename="sector")
router.register(r'company', CompanyViewSet, basename="company")

urlpatterns = router.urls
