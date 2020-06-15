"""tellme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from news.views import NewsViewset
from users.views import UserViewset
from notifications.views import NotificationViewset, MarkAllNotificationView
from articles.views import ArticleViewset, DraftViewset, MarkdonViewset, CommentViewset, TagViewset
from qa.views import QuestionViewset, AnswerViewset, VoteViewset
from messenger.views import MessageViewset
from search.views import ArticleSearchViewSet, UserSearchViewSet, NewsSearchViewSet, QuestionSearchViewSet
from upload.views import FileUploadView, UserPictureUploadView
from tellme.settings import MEDIA_ROOT

router = DefaultRouter()
router.register(r'news', NewsViewset, basename='news')
router.register(r'user', UserViewset, basename='user')
router.register(r'notification', NotificationViewset, basename='notification')
router.register(r'article', ArticleViewset, basename='article')
router.register(r'draft', DraftViewset, basename='draft')
router.register(r'question', QuestionViewset, basename='question')
router.register(r'answer', AnswerViewset, basename='answer')
router.register(r'vote', VoteViewset, basename='vote')
router.register(r'message', MessageViewset, basename='message')
router.register(r'comment', CommentViewset, basename='comment')
router.register(r'search/article', ArticleSearchViewSet, basename='search-article')
router.register(r'search/user', UserSearchViewSet, basename='search-user')
router.register(r'search/news', NewsSearchViewSet, basename='search-news')
router.register(r'search/question', QuestionSearchViewSet, basename='search-question')

router.register(r'tags', TagViewset, basename='tags')


urlpatterns = [
    url(r'^', include(router.urls)),
    path('admin/', admin.site.urls),
    url(r'^docs/', include_docs_urls(title='TellMe API Doc')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    path('^markdownx/', include('markdownx.urls')),
    url(r'^markdown/', csrf_exempt(MarkdonViewset.as_view())),
    url(r'^notification-markall/', MarkAllNotificationView.as_view()),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^upload/', FileUploadView.as_view()),
    url(r'^upload-user-picture/', UserPictureUploadView.as_view()),
    url(r'^api-token-verify/', verify_jwt_token),
    url('', include('social_django.urls', namespace='social')),
]

urlpatterns = [
    url(r'^api/', include(urlpatterns)),
]
