from rest_framework.routers import DefaultRouter
from .views import PortfolioView

app_name = "portfolio_api"

router = DefaultRouter()
router.register(r'portfolio', PortfolioView, basename="portfolio")

urlpatterns = router.urls
