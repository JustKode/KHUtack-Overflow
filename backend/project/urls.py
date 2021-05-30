from project.views import main
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', main, name='index'),
    path('admin/', admin.site.urls),
    path('martor/', include('martor.urls')),
    path('board/', include('board.urls')),
    path('post/', include('post.urls')),
    path('user/', include('user.urls')),
    path('file/', include('file.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)