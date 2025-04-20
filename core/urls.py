# from django.contrib import admin
# from django.urls import path, include
# from dashboard import views
# from . import views
# from django.conf import settings
# from django.conf.urls.static import static
# from .views import login_view

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # path('', include('dashboard.urls')),
#     path('', views.dashboard_view, name='dashboard'),
#     path('signup/', views.signup_view, name='signup'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('dashboard/', include('dashboard.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
