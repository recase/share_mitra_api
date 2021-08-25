from rest_framework.routers import DefaultRouter
from .views import AlertView, PortfolioView, TargetStopLossView, TransactionView, WatchListView

app_name = "portfolio_api"

router = DefaultRouter()
router.register(r'portfolio', PortfolioView, basename="portfolio")
router.register(r'portfolio-transaction',
                TransactionView, basename="transaction")
router.register(r'alert', AlertView, basename='alert')
router.register(r'watchlist', WatchListView, basename='watchlist')
router.register(r'target-loss', TargetStopLossView, basename='target-loss')

urlpatterns = router.urls
