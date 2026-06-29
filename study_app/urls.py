from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generate_materials, name='generate_materials'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='study_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('export/word/<int:material_id>/', views.export_word, name='export_word'),
    path('shared/<uuid:share_id>/', views.shared_material, name='shared_material'),
    path('toggle_favorite/<int:material_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('toggle_mastered/<int:material_id>/', views.toggle_mastered, name='toggle_mastered'),
    path('update_tags/<int:material_id>/', views.update_tags, name='update_tags'),
    path('document_chat/<int:material_id>/', views.document_chat, name='document_chat'),
    path('translate_content/<int:material_id>/', views.translate_content, name='translate_content'),
    path('eli5_content/<int:material_id>/', views.eli5_content, name='eli5_content'),
    path('delete_material/<int:material_id>/', views.delete_material, name='delete_material'),
    path('get_raw_video_url/<str:video_id>/', views.get_raw_video_url, name='get_raw_video_url'),
]
