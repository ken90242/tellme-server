from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from .models import Question, Answer, Vote
from users.serializers import UserSerializer, checkUserAuthSerializer

class VoteItemDetailSerializer(serializers.ModelSerializer):
    user = checkUserAuthSerializer(read_only=True)

    class Meta:
        model = Vote
        fields = "__all__"


class VoteItemUpdateSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return VoteItemDetailSerializer(instance, context=self.context).data

    class Meta:
        model = Vote
        fields = ["value"]

class VoteItemCreateSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    pk = serializers.CharField()

    def to_representation(self, instance):
        return VoteItemDetailSerializer(instance, context=self.context).data

    class Meta:
        model = Vote
        fields = ["value", "category", "pk"]
    
    def validate(self, attrs):
        model_name = attrs.pop("category").lower()
        primary_key = attrs.pop("pk").lower()

        category = ContentType.objects.filter(model=model_name)
        if not category:
            raise ValidationError("category does not exist")
        attrs["content_type"] = category[0]

        if model_name == 'question':
            question = Question.objects.filter(slug=primary_key)
            if not question:
                raise ValidationError("target question does not exist")
            attrs['object_id'] = question[0].id
        elif model_name == 'answer':
            if not Answer.objects.filter(uuid_id=primary_key):
                raise ValidationError("target answer does not exist")
            attrs['object_id'] = primary_key

        
        attrs["user"] = self.context['request'].user

        return attrs


class AnswerDetailSerializer(serializers.ModelSerializer):
    total_votes = serializers.ReadOnlyField()
    user = UserSerializer()
    votes = VoteItemDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Answer
        fields = "__all__"


class AnswerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        # user, question
        fields = ["is_answer"]
    
    # def update(self, validated_data):
        # is_answer -> restricted

class AnswerCreateSerializer(serializers.ModelSerializer):
    question_slug = serializers.CharField(max_length=80)
    class Meta:
        model = Answer
        fields = ["content", "question_slug"]
        extra_kwargs = {
            'question_slug': {'write_only': True},
        }
    
    def to_representation(self, instance):
        return AnswerDetailSerializer(instance, context=self.context).data

    def validate(self, attrs):
        attrs["user"] = self.context['request'].user
        target_question = Question.objects.filter(slug=attrs.pop("question_slug"))
        if not target_question:
            raise ValidationError("question does not exist")
        attrs["question"] = target_question[0]

        return attrs
        

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        # user, question
        fields = ["user", "content", "question", "is_answer"]
    
    # def update(self, validated_data):
        # is_answer -> restricted
        

class QuestionSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    def validate(self, attrs):
        attrs["user"] = self.context['request'].user
        return attrs

    class Meta:
        model = Question
        fields = ["title", "content", "tags", "status"]

class QuestionDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    votes = VoteItemDetailSerializer(many=True, read_only=True)
    answer = AnswerDetailSerializer(many=True)
    total_votes = serializers.ReadOnlyField()
    has_answer = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    user = UserSerializer()

    class Meta:
        model = Question
        fields = "__all__"
