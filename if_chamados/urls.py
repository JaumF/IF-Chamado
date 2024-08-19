from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('if_app.urls')),
    path('if-dados/', include('if_dados.urls')),
]
