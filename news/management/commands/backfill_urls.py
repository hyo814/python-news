"""
기존 크롤링 글의 빈 source_url을 RSS 피드에서 다시 매칭하여 복구합니다.

사용법: python manage.py backfill_urls
"""

import feedparser
from django.core.management.base import BaseCommand
from news.models import Post

RSS_FEEDS = [
    "https://blog.python.org/feeds/posts/default?alt=rss",
    "https://www.djangoproject.com/rss/weblog/",
    "https://realpython.com/atom.xml",
    "https://planetpython.org/rss20.xml",
    "https://news.hada.io/rss/news",
    "https://meetup.nhncloud.com/rss",
    "https://techblog.woowahan.com/feed/",
    "https://engineering.linecorp.com/ko/feed/",
    "https://toss.tech/rss.xml",
]


class Command(BaseCommand):
    help = "크롤링 글 중 빈 source_url을 RSS 피드에서 매칭하여 복구"

    def handle(self, *args, **options):
        posts = Post.objects.filter(source_type="crawled", source_url="")
        if not posts.exists():
            self.stdout.write("복구할 글이 없습니다.")
            return

        self.stdout.write(f"source_url이 비어있는 글: {posts.count()}개\n")

        # 모든 피드에서 title → link 매핑 수집
        title_to_url = {}
        for feed_url in RSS_FEEDS:
            self.stdout.write(f"피드 수집: {feed_url}")
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    title = entry.get("title", "").strip()
                    link = entry.get("link", "")
                    if title and link:
                        title_to_url[title] = link
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  실패: {e}"))

        self.stdout.write(f"\n피드에서 수집된 항목: {len(title_to_url)}개\n")

        updated = 0
        for post in posts:
            url = title_to_url.get(post.title)
            if url:
                post.source_url = url
                post.save(update_fields=["source_url"])
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"  복구: {post.title}"))
            else:
                self.stdout.write(f"  매칭 실패: {post.title}")

        self.stdout.write(
            self.style.SUCCESS(f"\n완료! {updated}/{posts.count()}개 복구")
        )
