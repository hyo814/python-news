"""
주간 파이썬 백엔드 뉴스 크롤러.

RSS 피드에서 최신 글을 수집하여 DB에 저장합니다.
사용법: python manage.py crawl_news
스케줄링: crontab에 등록하여 매주 자동 실행
"""

import feedparser
from datetime import date, datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from bs4 import BeautifulSoup
from news.models import Post, Tag


RSS_FEEDS = [
    # 영어 소스
    {
        "url": "https://blog.python.org/feeds/posts/default?alt=rss",
        "source": "Python Blog",
        "tags": ["Python"],
    },
    {
        "url": "https://www.djangoproject.com/rss/weblog/",
        "source": "Django Blog",
        "tags": ["Django"],
    },
    {
        "url": "https://realpython.com/atom.xml",
        "source": "Real Python",
        "tags": ["Python"],
    },
    {
        "url": "https://planetpython.org/rss20.xml",
        "source": "Planet Python",
        "tags": ["Python"],
    },
    {
        "url": "https://pythonweekly.com/rss.xml",
        "source": "Python Weekly",
        "tags": ["Python"],
    },
    # 한국어 소스
    {
        "url": "https://news.hada.io/rss/news",
        "source": "GeekNews",
        "tags": ["Python"],
    },
    {
        "url": "https://www.44bits.io/ko/rss",
        "source": "44bits",
        "tags": ["Python", "DevOps"],
    },
    {
        "url": "https://meetup.nhncloud.com/rss",
        "source": "NHN Cloud Meetup",
        "tags": ["Python"],
    },
    {
        "url": "https://techblog.woowahan.com/feed/",
        "source": "우아한형제들 기술블로그",
        "tags": ["Python"],
    },
    {
        "url": "https://engineering.linecorp.com/ko/feed/",
        "source": "LINE Engineering",
        "tags": ["Python"],
    },
    {
        "url": "https://toss.tech/rss.xml",
        "source": "Toss Tech",
        "tags": ["Python"],
    },
]

# 한국어 소스에서 파이썬 관련 글만 필터링하기 위한 키워드
PYTHON_KEYWORDS = [
    "python", "파이썬", "django", "fastapi", "flask",
    "celery", "sqlalchemy", "pydantic", "uvicorn", "gunicorn",
    "pip", "poetry", "pytest", "asyncio", "백엔드", "backend",
]


class Command(BaseCommand):
    help = "RSS 피드에서 파이썬 백엔드 관련 뉴스를 크롤링합니다"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=7,
            help="최근 N일 이내의 글만 수집 (기본: 7)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="DB에 저장하지 않고 수집 결과만 출력",
        )

    def handle(self, *args, **options):
        days = options["days"]
        dry_run = options["dry_run"]
        cutoff = datetime.now() - timedelta(days=days)
        total_created = 0

        self.stdout.write(f"\n크롤링 시작 (최근 {days}일 이내 글 수집)\n")

        for feed_config in RSS_FEEDS:
            created = self._process_feed(feed_config, cutoff, dry_run)
            total_created += created

        self.stdout.write(
            self.style.SUCCESS(f"\n완료! 총 {total_created}개 새 글 저장\n")
        )

    def _process_feed(self, feed_config, cutoff, dry_run):
        url = feed_config["url"]
        source = feed_config["source"]
        tag_names = feed_config["tags"]
        is_korean_source = source in (
            "GeekNews", "44bits", "NHN Cloud Meetup",
            "우아한형제들 기술블로그", "LINE Engineering", "Toss Tech",
        )

        self.stdout.write(f"\n[{source}] {url}")

        try:
            feed = feedparser.parse(url)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"  피드 파싱 실패: {e}"))
            return 0

        if not feed.entries:
            self.stdout.write("  항목 없음")
            return 0

        created_count = 0
        for entry in feed.entries[:15]:
            result = self._process_entry(
                entry, source, tag_names, cutoff, dry_run, is_korean_source
            )
            if result:
                created_count += 1

        self.stdout.write(
            f"  {min(len(feed.entries), 15)}개 확인, {created_count}개 신규"
        )
        return created_count

    def _process_entry(self, entry, source, tag_names, cutoff, dry_run, is_korean_source):
        title = entry.get("title", "").strip()
        if not title:
            return False

        # 한국어 소스는 파이썬 관련 글만 필터링
        if is_korean_source:
            search_text = (title + " " + entry.get("summary", "")).lower()
            if not any(kw in search_text for kw in PYTHON_KEYWORDS):
                return False

        published = self._parse_date(entry)
        if published and published < cutoff:
            return False

        slug = slugify(title, allow_unicode=True)[:200]
        if not slug:
            slug = slugify(f"{source}-{title[:50]}", allow_unicode=True)[:200]

        if Post.objects.filter(slug=slug).exists():
            return False

        summary = self._extract_summary(entry)
        content = self._extract_content(entry)
        pub_date = published.date() if published else date.today()
        source_url = entry.get("link", "")

        if dry_run:
            self.stdout.write(f"  [DRY RUN] {title}")
            return True

        post = Post.objects.create(
            title=title,
            slug=slug,
            summary=summary,
            content=content,
            author=source,
            published_at=pub_date,
            source_type="crawled",
            source_url=source_url,
        )

        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(
                name=tag_name,
                defaults={"slug": slugify(tag_name, allow_unicode=True)},
            )
            post.tags.add(tag)

        self._auto_tag(post, title + " " + summary)
        self.stdout.write(self.style.SUCCESS(f"  + {title}"))
        return True

    def _parse_date(self, entry):
        for attr in ("published_parsed", "updated_parsed"):
            parsed = entry.get(attr)
            if parsed:
                try:
                    return datetime(*parsed[:6])
                except (TypeError, ValueError):
                    continue
        return None

    def _extract_summary(self, entry):
        summary = entry.get("summary", "")
        if summary:
            soup = BeautifulSoup(summary, "html.parser")
            text = soup.get_text(strip=True)
            return text[:300] + ("..." if len(text) > 300 else "")
        return entry.get("title", "")

    def _extract_content(self, entry):
        for field in ("content", "summary_detail"):
            data = entry.get(field)
            if isinstance(data, list) and data:
                html = data[0].get("value", "")
            elif hasattr(data, "value"):
                html = data.value
            else:
                continue

            if html:
                soup = BeautifulSoup(html, "html.parser")
                return soup.get_text(separator="\n\n", strip=True)

        return entry.get("summary", entry.get("title", ""))

    def _auto_tag(self, post, text):
        """본문/제목 키워드를 분석하여 자동으로 태그 추가"""
        keyword_tags = {
            "Django": ["django", "drf", "django rest"],
            "FastAPI": ["fastapi", "starlette"],
            "Flask": ["flask"],
            "Database": ["postgres", "mysql", "sqlite", "database", "sql", "orm",
                         "sqlalchemy", "데이터베이스"],
            "DevOps": ["docker", "kubernetes", "k8s", "ci/cd", "deploy", "aws",
                        "배포", "인프라"],
            "Testing": ["pytest", "unittest", "test", "tdd", "테스트"],
            "AI/ML": ["machine learning", "ai", "llm", "openai", "langchain", "ml",
                       "머신러닝", "딥러닝"],
        }

        text_lower = text.lower()
        for tag_name, keywords in keyword_tags.items():
            if any(kw in text_lower for kw in keywords):
                tag, _ = Tag.objects.get_or_create(
                    name=tag_name,
                    defaults={"slug": slugify(tag_name, allow_unicode=True)},
                )
                post.tags.add(tag)
