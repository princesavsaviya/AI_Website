"""
URL configuration for nimbus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from genimg import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('generate-image/landscape', views.generate_img, name='generate_image'),
    path('generate-image/living-object', views.generate_img_2, name='generate_image_2'),
    path('previous-image/', views.previous_image, name='previous_image'),  
    path('display-image/', views.display_image, name='display_image'), 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
