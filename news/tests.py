from datetime import datetime, timedelta

from django.test import TestCase

from news.management.commands.crawl_news import Command
from news.models import Post


class CrawlNewsCommandTests(TestCase):
    def test_process_entry_marks_new_crawled_posts_curated(self):
        command = Command()
        entry = {
            "title": "FastAPI 배포 가이드",
            "summary": "<p>FastAPI 운영과 pytest 팁</p>",
            "link": "https://example.com/posts/fastapi-deploy",
            "published_parsed": datetime.now().timetuple(),
        }

        created = command._process_entry(
            entry=entry,
            source="Real Python",
            tag_names=["Python"],
            cutoff=datetime.now() - timedelta(days=7),
            dry_run=False,
            is_korean_source=False,
        )

        self.assertTrue(created)
        post = Post.objects.get(source_url=entry["link"])
        self.assertTrue(post.is_curated)
