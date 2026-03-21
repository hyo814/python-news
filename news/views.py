from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Tag, Subscriber
from .serializers import (
    PostListSerializer, PostDetailSerializer,
    TagSerializer, SubscribeSerializer,
)


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):

        qs = Post.objects.prefetch_related("tags")

        # 크롤링 글은 큐레이션된 것만 노출, 에디토리얼은 전부 노출
        qs = qs.filter(
            Q(source_type="editorial") | Q(source_type="crawled", is_curated=True)
        )

        source_type = self.request.query_params.get("type")
        if source_type in ("editorial", "crawled"):
            qs = qs.filter(source_type=source_type)
        tag = self.request.query_params.get("tag")
        if tag:
            qs = qs.filter(tags__slug=tag)
        return qs


class PostDetailView(generics.RetrieveAPIView):
    serializer_class = PostDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):

        return Post.objects.prefetch_related("tags").filter(
            Q(source_type="editorial") | Q(source_type="crawled", is_curated=True)
        )


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class FeaturedPostView(generics.ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):

        return Post.objects.filter(is_featured=True).prefetch_related("tags").filter(
            Q(source_type="editorial") | Q(source_type="crawled", is_curated=True)
        )


class SubscribeView(APIView):
    def post(self, request):
        serializer = SubscribeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "구독이 완료되었습니다!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnsubscribeView(APIView):
    def post(self, request):
        token = request.data.get("token")
        try:
            subscriber = Subscriber.objects.get(token=token)
            subscriber.is_active = False
            subscriber.save()
            return Response({"message": "구독이 해지되었습니다."})
        except Subscriber.DoesNotExist:
            return Response(
                {"error": "유효하지 않은 토큰입니다."},
                status=status.HTTP_404_NOT_FOUND,
            )
