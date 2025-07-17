# empregasenac/urls.py
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('minhas-vagas/', include('app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('vagas-publicas/', views.VagaPublicaListView.as_view(), name='vagas_publicas'),  # Adicione esta linha
    # REMOVE THIS LINE: path('vagas-publicas/', include('app.urls')),
]

# Adicione esta condição APENAS para ambiente de desenvolvimento.
# Em produção, um servidor web (Nginx, Apache) serve os arquivos de mídia.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)