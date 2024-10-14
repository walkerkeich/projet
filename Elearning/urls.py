from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('utilisateurs.urls')),         # Inclure les URLs de l'application utilisateurs
    path('programmes/', include('app.urls')),       # Inclure les URLs de l'application principale
    path('api/', include('app.api.urls')),
    
    path('api/users/', include('utilisateurs.api_user.urls')), # Inclure les URLs de l'API

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
