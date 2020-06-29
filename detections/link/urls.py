from . import views
from django.urls import path

urlpatterns = [
    path('',views.index,name = 'index'),
    path('badwords',views.badwords,name = 'badwords'),
    path('run',views.run,name = 'run'),
    path('badwords/<int:id>',views.remove,name = 'remove'),
]
