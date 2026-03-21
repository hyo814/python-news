import uuid
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    class SourceType(models.TextChoices):
        EDITORIAL = "editorial", "직접 작성"
        CRAWLED = "crawled", "크롤링"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    summary = models.TextField(help_text="글 요약 (목록에 표시)")
    content = models.TextField(help_text="본문 (Markdown 지원)")
    cover_image = models.ImageField(upload_to="covers/", blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    author = models.CharField(max_length=100, default="PyNews 팀")
    source_type = models.CharField(
        max_length=10,
        choices=SourceType.choices,
        default=SourceType.EDITORIAL,
    )
    source_url = models.URLField(blank=True, help_text="원본 링크 (크롤링 글)")
    published_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
