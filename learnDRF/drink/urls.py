from django.urls import path, re_path

from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenVerifyView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views
from .views import LoginView, LogoutView, RegisterUserView, NoteView, NoteDetailView, NotebookView, NotebookDetailView, CreateNoteView, MoveNoteToTrash, RestoreNoteFromTrash, DeleteNotePermanently, TrashBinView

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API documentation for My App",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", views.home, name="home"),
    path("developer/", views.developer, name="developer"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('Logout',LogoutView.as_view(), name="logout"),

    path('note/', views.note, name='note'),
    path('note/<int:note_id>/', views.mynote, name='mynote'),
    path('createnote/<int:notebook_id>/', views.createnote, name='createnote'),
    path('trashbin', views.trashbin, name='trashbin'),

    # api
    path('api/notebooks/', NotebookView.as_view(), name='notebook-list'),
    path('api/notebooks/<int:pk>/', NotebookDetailView.as_view(), name='notebook-detail'),

    path('api/notebooks/<int:notebook_id>/notes/', CreateNoteView.as_view(), name='create-note'),

    path('api/notes/', NoteView.as_view(), name='notes_api'),
    path('api/notes/<int:pk>/', NoteDetailView.as_view(), name='note_detail'),

    path('api/trash_bin/', TrashBinView.as_view(), name='trash_bin'),
    path('api/move_to_trash/<int:note_id>/', MoveNoteToTrash.as_view(), name='move_to_trash'),
    path('api/restore_from_trash/<int:note_id>/', RestoreNoteFromTrash.as_view(), name='restore_from_trash'),
    path('api/delete_note/<int:note_id>/', DeleteNotePermanently.as_view(), name='delete_note_permanently'),

    #jwt
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    #redoc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('download/note/<int:note_id>/', views.download_note, name='download_note'),


]