from django.shortcuts import render

from rest_framework import mixins
from rest_framework import viewsets

from notifications.views import notification_handler
from .models import Question, Answer, Vote
from .serializers import QuestionSerializer, QuestionDetailSerializer, VoteItemCreateSerializer, VoteItemUpdateSerializer
from .serializers import AnswerSerializer, AnswerDetailSerializer, AnswerUpdateSerializer, AnswerCreateSerializer
from .filters import QuestionFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from django.contrib.contenttypes.models import ContentType


# Create your views here.
class QuestionViewset(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    filter_class = QuestionFilter
    lookup_field = 'slug'
    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return QuestionSerializer
        return QuestionDetailSerializer

class AnswerViewset(mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Answer.objects.all().order_by('-created_at')
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_serializer_class(self):
        if self.action == "create":
            return AnswerCreateSerializer
        elif self.action == "update":
            return AnswerUpdateSerializer
        return AnswerDetailSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()
        q = Question.objects.filter(id=serializer.data['question'])
        print(q[0].user.username)
        if q:
            if q[0].user.username != self.request.user.username:
                print(self.request.user, q[0].user)
                notification_handler(self.request.user, q[0].user, 'A', q[0])

class VoteViewset(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, )

    def get_queryset(self, *args, **kwargs):
        if self.action == 'list':
            request = self.request
            queryset = Vote.objects.all()

            if not request.GET.get('category') or not request.GET.get('pk'):
                return Vote.objects.none()

            model_name = request.GET.get('category')
            primary_key = request.GET.get('pk')
            category = ContentType.objects.filter(model=model_name)
            if not category:
                return Vote.objects.none()

            queryset = queryset.filter(user=request.user, content_type=category[0])
            if model_name == 'question':
                question = Question.objects.filter(slug=primary_key)
                if not question:
                    return Vote.objects.none()

                queryset = queryset.filter(object_id=question[0].id)

            elif model_name == 'answer':
                answer = Answer.objects.filter(uuid_id=primary_key)
                if not answer:
                    return Vote.objects.none()
                
                queryset = queryset.filter(object_id=answer[0].uuid_id)
        else:
            queryset = Vote.objects.all()
        
        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return VoteItemCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return VoteItemUpdateSerializer
        elif self.action == "list":
            return VoteItemUpdateSerializer
        return VoteItemCreateSerializer
