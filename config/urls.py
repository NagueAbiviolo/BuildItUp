<<<<<<< HEAD
from django.contrib import admin
from django.urls import path, include
from app.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("auth/", include("app.urls")),
]
=======
from django.contrib import admin
from django.urls import path, include
from app.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("auth/", include("app.urls")),
]
>>>>>>> 0b70f733a5fbdca43ff5f98bde71b74d625c3dbb
