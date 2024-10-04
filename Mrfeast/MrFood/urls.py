from django.contrib import admin
from django.urls import path, include
from food import views as foodViews
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='inicio.html'), name='inicio'),
    path('user/', include('user.urls')),
    path('portal/', include('food.urls')),  # Include all food-related URLs
    path('form/', foodViews.HomeView.as_view(), name='form'),
    path('contacto/', foodViews.ContactoView.as_view(), name='contacto'),
    path('generar/', foodViews.GenerarView.as_view(), name='generar'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
