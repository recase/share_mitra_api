from rest_framework.routers import DefaultRouter
from .views import LivePirceViewSet, SectorViewSet, CompanyViewSet, StockPriceViewSet

app_name = "stock_api"

router = DefaultRouter()
router.register(r'sector', SectorViewSet, basename="sector")
router.register(r'company', CompanyViewSet, basename="company")
router.register(r'live-pirce', LivePirceViewSet, basename="live-price")
router.register(r'stock-price', StockPriceViewSet, basename="stock-price")

urlpatterns = router.urls
