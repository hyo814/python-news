"""
주간 뉴스레터 이메일 발송.

구독자들에게 이번 주 수집된 글 목록을 이메일로 전송합니다.
사용법: python manage.py send_newsletter
"""

from datetime import date, timedelta
from django.core.mail import send_mass_mail
from django.core.management.base import BaseCommand
from news.models import Post, Subscriber


class Command(BaseCommand):
    help = "구독자들에게 주간 뉴스레터를 발송합니다"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=7,
            help="최근 N일간의 글 포함 (기본: 7)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="실제 발송 없이 내용만 확인",
        )

    def handle(self, *args, **options):
        days = options["days"]
        dry_run = options["dry_run"]

        cutoff = date.today() - timedelta(days=days)
        posts = Post.objects.filter(published_at__gte=cutoff).order_by("-published_at")
        subscribers = Subscriber.objects.filter(is_active=True)

        if not posts.exists():
            self.stdout.write("발송할 새 글이 없습니다.")
            return

        if not subscribers.exists():
            self.stdout.write("활성 구독자가 없습니다.")
            return

        subject = f"[PyNews] {date.today().strftime('%Y-%m-%d')} 주간 파이썬 백엔드 소식"
        body = self._build_body(posts)

        self.stdout.write(f"\n제목: {subject}")
        self.stdout.write(f"글 수: {posts.count()}개")
        self.stdout.write(f"구독자 수: {subscribers.count()}명\n")

        if dry_run:
            self.stdout.write("--- 뉴스레터 내용 ---")
            self.stdout.write(body)
            self.stdout.write("--- 끝 ---\n")
            self.stdout.write("[DRY RUN] 실제 발송하지 않았습니다.")
            return

        messages = []
        for sub in subscribers:
            unsub_note = f"\n\n---\n구독 해지: 토큰 {sub.token}"
            messages.append((subject, body + unsub_note, None, [sub.email]))

        sent = send_mass_mail(messages, fail_silently=True)
        self.stdout.write(self.style.SUCCESS(f"발송 완료! {sent}건"))

    def _build_body(self, posts):
        lines = ["안녕하세요! PyNews 주간 뉴스레터입니다.\n"]
        lines.append(f"이번 주 {posts.count()}개의 새로운 소식을 전합니다.\n")

        editorial = posts.filter(source_type="editorial")
        crawled = posts.filter(source_type="crawled")

        if editorial.exists():
            lines.append("\n== 에디터 픽 ==\n")
            for post in editorial:
                tags = ", ".join(t.name for t in post.tags.all())
                lines.append(f"- {post.title} [{tags}]")
                lines.append(f"  {post.summary[:100]}\n")

        if crawled.exists():
            lines.append("\n== 커뮤니티 소식 ==\n")
            for post in crawled:
                source_info = f" ({post.source_url})" if post.source_url else ""
                lines.append(f"- {post.title}{source_info}")

        lines.append("\n\n읽어주셔서 감사합니다! - PyNews 팀")
        return "\n".join(lines)
