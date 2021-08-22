from rest_framework.routers import DefaultRouter
from .views import PortfolioView, TransactionView

app_name = "portfolio_api"

router = DefaultRouter()
router.register(r'portfolio', PortfolioView, basename="portfolio")
router.register(r'portfolio-transaction',
                TransactionView, basename="transaction")

urlpatterns = router.urls
