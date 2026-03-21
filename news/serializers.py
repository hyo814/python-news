from rest_framework import serializers
from .models import Tag, Post, Subscriber


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class PostListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "summary", "cover_image",
            "tags", "author", "published_at", "is_featured",
            "source_type", "source_url",
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "summary", "content", "cover_image",
            "tags", "author", "published_at", "created_at", "is_featured",
            "source_type", "source_url",
        ]


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ["email"]

    def validate_email(self, value):
        value = value.lower().strip()
        if Subscriber.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError("이미 구독 중인 이메일입니다.")
        return value

    def create(self, validated_data):
        email = validated_data["email"]
        subscriber, created = Subscriber.objects.get_or_create(
            email=email,
            defaults={"is_active": True},
        )
        if not created and not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save()
        return subscriber
