import markdown
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.middleware import csrf
from django.conf import settings
from django.views import View
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.renderers import TemplateHTMLRenderer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .forms import RegisterUserForm
from .serializers import NoteSerializer, NotebookSerializer
from .models import Note, Notebook


def home(request) -> HttpResponse:
    return render(request, 'home.html')

def note(request) -> HttpResponse:

    context = {
        'notebooks_api': 'http://127.0.0.1:8000/api/notebooks/',
    }
    return render(request, 'note.html', context)
    pass


def createnote(request, notebook_id: int) -> HttpResponse:
    context = {
        'notebook_id': notebook_id,
        'createnotes_api': 'http://127.0.0.1:8000/api/notebooks/',
        # 其他需要的上下文变量...
    }
    return render(request, 'createnote.html', context)

def trashbin(request) -> HttpResponse:

    return render(request, 'trashbin.html')

def download_note(request, note_id):
    # 根据ID获取笔记对象
    note = get_object_or_404(Note, id=note_id)

    # 创建HttpResponse对象，设置内容类型为text/plain
    response = HttpResponse(note.content, content_type='text/plain')

    # 设置HTTP头部以提示浏览器下载文件而不是显示它
    response['Content-Disposition'] = 'attachment; filename="{}.txt"'.format(note.title.replace(' ', '_'))

    return response


def mynote(request, note_id: int) -> HttpResponse:
    # 获取指定ID的笔记对象
    note = get_object_or_404(Note, id=note_id)

    # 将Markdown文本转换为HTML
    html_content = markdown.markdown(note.content)

    # 将转换后的HTML内容和其他需要的上下文变量传递到模板
    context = {
        'note_id': note_id,
        'html_content': html_content,
        'notes_api': 'http://127.0.0.1:8000/api/notes',
        # 其他需要的上下文变量...
    }
    return render(request, 'mynote.html', context)


def developer(request) -> HttpResponse:
    """Render the developer information page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered developer page.
    """
    return render(request, 'developer.html')
    pass


def get_tokens_for_user(user) -> dict:
    """Get JWT tokens for authentication of a user.

    Args:
        user: The user object for which to create tokens.

    Returns:
        dict: A dictionary containing the refresh and access tokens.
    """
    refresh = RefreshToken.for_user(user)  # 为用户创建新的刷新token
    return {
        'refresh': str(refresh),  # 刷新token
        'access': str(refresh.access_token),  # 访问token
    }
    pass


class RegisterUserView(View):
    template_name = "register.html"  # 指定使用的模板文件
    form_class = RegisterUserForm  # 指定使用的表單

    # 處理GET請求
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    # 處理POST請求
    def post(self, request):
        form = self.form_class(request.POST)  # 獲取POST表單數據
        if form.is_valid():  # 驗證表單
            user = form.save()  # 保存新用戶
            # 為新用戶創建筆記本
            Notebook.objects.create(user=user, name="Default Notebook")
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)  # 驗證用戶
            login(request, user)  # 登錄用戶
            return render(request, "login.html")  # 重定向至登錄頁面
        else:
            return render(request, self.template_name, {"form": form})  # 表單無效時重新渲染註冊頁面

# 登錄
class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]  # 設置渲染器
    template_name = 'login.html'  # 指定使用的模板文件
    permission_classes = []  # 無特定權限要求

    # 處理GET請求
    def get(self, request):
        return Response()

    # 處理POST請求
    def post(self, request):
        data = request.data  # 獲取請求數據
        username = data.get('username', None)  # 獲取用戶名
        password = data.get('password', None)  # 獲取密碼
        user = authenticate(request, username=username, password=password)  # 驗證用戶
        if user is not None:  # 如果用戶驗證成功
            login(request, user)
            tokens = get_tokens_for_user(user)  # 獲取用戶token
            response = redirect(note)  # 重定向至筆記
            # 設置cookie存儲JWT令牌
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],  # Cookie名
                value=tokens["access"],  # token
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],  # 過期時間
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],  # 是否僅通過HTTPS發送
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],  # 防止JavaScript訪問
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']  # 防止CSRF攻擊
            )
            #csrf.get_token(request)

            response.data = {"Success": "Login successfully", "tokens": tokens}  # 設置響應數據

            return response  # 返回響應，重定向至筆記頁面
        else:
            # 登錄失敗，返回錯誤信息
            return Response({'error': 'Wrong credentials'}, status=400, template_name='login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)  # 清除会话
        response = redirect('home')  # 重定向到首页或其他适当的页面
        response.delete_cookie('access_token')  # 清除存储JWT的Cookie
        messages.success(request, "You were logged out")
        return response


class CustomAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)  # 從header中獲取token

        if header is None:
            # 如果header中沒有令牌，嘗試從cookie中獲取
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
        else:
            raw_token = self.get_raw_token(header)  # 從header中獲取原始token
        if raw_token is None:
            return None  # 如果沒有token，返回None

        validated_token = self.get_validated_token(raw_token)  # 驗證token
        return self.get_user(validated_token), validated_token  # 返回用戶和驗證過的token


class CreateNoteView(APIView):
    authentication_classes = [CustomAuthentication]  # 使用自定義JWT認證
    permission_classes = [IsAuthenticated]  # 要求用戶必須認證

    def get(self, request, notebook_id):
        try:
            notebook = Notebook.objects.get(id=notebook_id)
            notes = Note.objects.filter(notebook=notebook)
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Notebook.DoesNotExist:
            return Response({'error': 'Notebook not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, notebook_id):
        try:
            notebook = Notebook.objects.get(id=notebook_id)
        except Notebook.DoesNotExist:
            return Response({'error': 'Notebook not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(notebook=notebook)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Notebook API
class NotebookView(APIView):
    authentication_classes = [CustomAuthentication]  # 使用自定義JWT認證
    permission_classes = [IsAuthenticated]  # 要求用戶必須認證

    @swagger_auto_schema(responses={200: NotebookSerializer(many=True)})
    def get(self, request):
        notebooks = Notebook.objects.filter(user=request.user)  # 獲取當前用戶的所有筆記本
        serializer = NotebookSerializer(notebooks, many=True)  # 序列化筆記本數據
        return Response(serializer.data)  # 返回筆記本數據

    @swagger_auto_schema(request_body=NotebookSerializer(), responses={201: NotebookSerializer()})
    def post(self, request):
        # 創建筆記本
        serializer = NotebookSerializer(data=request.data)  # 獲取請求數據進行序列化
        if serializer.is_valid():  # 如果數據有效
            serializer.save(user=request.user)  # 保存筆記本，關聯到當前用戶
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # 返回新創建的筆記本數據
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 返回錯誤信息


class NotebookDetailView(APIView):
    authentication_classes = [CustomAuthentication]  # 使用自定義JWT
    permission_classes = [IsAuthenticated]  # 要求用戶必須認證

    def get_object(self, pk):
        notebook = Notebook.objects.filter(user=self.request.user)
        return get_object_or_404(notebook, pk=pk)

    @swagger_auto_schema(responses={200: NotebookSerializer()})
    def get(self, request, pk):
        notebook = self.get_object(pk)
        serializer = NotebookSerializer(notebook)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=NotebookSerializer(), responses={200: NotebookSerializer()})
    def put(self, request, pk):
        notebook = self.get_object(pk)
        serializer = NotebookSerializer(notebook, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'Notebook deleted'})
    def delete(self, request, pk):
        notebook = self.get_object(pk)
        notebook.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Note API
class NoteView(APIView):
    authentication_classes = [CustomAuthentication]  # 使用自定義JWT
    permission_classes = [IsAuthenticated]  # 要求用戶必須認證

    @swagger_auto_schema(responses={200: NoteSerializer(many=True)})
    def get(self, request):
        notebooks = Notebook.objects.filter(user=request.user)  # 獲取當前用戶的所有筆記本
        notes = Note.objects.filter(notebook__in=notebooks, is_trashed=False)  # 從這些用戶筆記本本中獲取所有筆記，且不在垃圾筒的筆記
        serializer = NoteSerializer(notes, many=True)  # 序列化筆記數據
        return Response(serializer.data)  # 返回筆記數據

    @swagger_auto_schema(request_body=NoteSerializer())  
    def post(self, request):
        serializer = NoteSerializer(data=request.data)  # 獲取請求數據進行序列化
        if serializer.is_valid():  # 如果數據有效
            notebook = Notebook.objects.filter(user=request.user).first()  # 獲取用戶的第一個筆記本
            if not notebook:
                # 如果用戶沒有筆記本，返回404錯誤
                return Response({'error': 'No notebook found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer.save(notebook=notebook)  # 保存筆記，關聯到筆記本
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # 返回新創建的筆記數據
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 返回錯誤信息

# URD視圖
class NoteDetailView(APIView):
    authentication_classes = [CustomAuthentication]  # 使用自定義JWT認證
    permission_classes = [IsAuthenticated]  # 要求用戶必須認證

    def get_object(self, pk):
        # 根據主鍵ID獲取筆記對象
        notebooks = Notebook.objects.filter(user=self.request.user)
        return get_object_or_404(Note, pk=pk, notebook__in=notebooks)

    @swagger_auto_schema(responses={200: NoteSerializer()})
    def get(self, request, pk):

        note = self.get_object(pk)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=NoteSerializer(), responses={200: NoteSerializer()})
    def put(self, request, pk):

        note = self.get_object(pk)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'Note deleted'})
    def delete(self, request, pk):

        note = self.get_object(pk)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TrashBinView(APIView):
    authentication_classes = [CustomAuthentication]  # 使用自定義JWT認證
    permission_classes = [IsAuthenticated]  # 要求用戶必須認證

    def get(self, request):
        trashed_notes = Note.objects.filter(is_trashed=True)
        serializer = NoteSerializer(trashed_notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MoveNoteToTrash(APIView):
    authentication_classes = [CustomAuthentication]  # 使用自定義JWT認證
    permission_classes = [IsAuthenticated]  # 要求用戶必須認證

    def post(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        note.is_trashed = True
        note.save()
        return Response({'status': 'success', 'message': 'Note moved to trash'}, status=status.HTTP_200_OK)

class RestoreNoteFromTrash(APIView):
    authentication_classes = [CustomAuthentication]  # 使用自定義JWT認證
    permission_classes = [IsAuthenticated]  # 要求用戶必須認證

    def post(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        note.is_trashed = False
        note.save()
        return Response({'status': 'success', 'message': 'Note restored from trash'}, status=status.HTTP_200_OK)

class DeleteNotePermanently(APIView):
    authentication_classes = [CustomAuthentication]  # 使用自定義JWT認證
    permission_classes = [IsAuthenticated]  # 要求用戶必須認證

    def delete(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        note.delete()
        return Response({'status': 'success', 'message': 'Note permanently deleted'}, status=status.HTTP_200_OK)