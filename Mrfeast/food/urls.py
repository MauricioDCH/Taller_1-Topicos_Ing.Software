from django.urls import path
from .views import PortalView, MenuDetailView, CreateReviewView, UpdateReviewView, DeleteReviewView, BuscarView

urlpatterns = [
    path('', PortalView.as_view(), name='portal'),
    path('buscar/', BuscarView.as_view(), name='buscar'),  # Añade esta línea
    path('menu/<int:pk>/', MenuDetailView.as_view(), name='detail'),
    path('menu/create/<int:menu_id>/', CreateReviewView.as_view(), name='createreview'),
    path('review/update/<int:pk>/', UpdateReviewView.as_view(), name='updatereview'),
    path('review/delete/<int:pk>/', DeleteReviewView.as_view(), name='deletereview'),

]
