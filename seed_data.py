import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from datetime import date
from news.models import Tag, Post

tags_data = ["Python", "Django", "FastAPI", "Flask", "DevOps", "Database", "Testing", "AI/ML"]
tags = {}
for name in tags_data:
    tag, _ = Tag.objects.get_or_create(name=name, slug=name.lower().replace("/", "-"))
    tags[name] = tag

posts = [
    {
        "title": "[PyNews] 2026-03 - Django 6.0의 새로운 기능 총정리",
        "slug": "pynews-2026-03",
        "summary": "Django 6.0이 정식 릴리스되었습니다. 비동기 ORM 지원 강화, 새로운 폼 렌더링 엔진, 그리고 성능 개선 사항을 살펴봅니다. 또한 FastAPI 0.115의 주요 변경점과 Python 3.14 프리뷰 소식도 함께 전합니다.",
        "content": """# Django 6.0 릴리스 하이라이트

## 비동기 ORM 완전 지원
Django 6.0에서 가장 주목할 만한 변화는 비동기 ORM의 완전한 지원입니다. 이제 `async for`를 사용한 QuerySet 순회가 네이티브로 지원되며, `select_related`와 `prefetch_related`도 비동기 컨텍스트에서 올바르게 동작합니다.

```python
async def get_posts():
    async for post in Post.objects.select_related('author').all():
        print(post.title)
```

## 새로운 폼 렌더링 엔진
`django.forms` 모듈이 컴포넌트 기반 렌더링 시스템으로 전환되었습니다. 이를 통해 커스텀 위젯 작성이 훨씬 간편해졌습니다.

## 성능 개선
- QuerySet 캐싱 메커니즘 개선으로 평균 15% 속도 향상
- 마이그레이션 실행 속도 2배 개선
- 정적 파일 서빙 최적화

---

# FastAPI 0.115 주요 변경점

FastAPI가 Pydantic v3 지원을 시작했습니다. 새로운 `TypeAdapter` API와의 통합으로 직렬화 성능이 크게 향상되었습니다.

---

# Python 3.14 프리뷰

PEP 768 (Incremental GC)이 승인되어 Python 3.14에 포함될 예정입니다. 가비지 컬렉션 pause time이 대폭 줄어들 것으로 기대됩니다.
""",
        "tags": ["Python", "Django", "FastAPI"],
        "published_at": date(2026, 3, 1),
        "is_featured": True,
    },
    {
        "title": "[PyNews] 2026-02 - FastAPI vs Django: 2026년 선택 가이드",
        "slug": "pynews-2026-02",
        "summary": "2026년 현재 FastAPI와 Django의 생태계를 비교 분석합니다. 각 프레임워크의 강점, 약점, 그리고 프로젝트 유형별 추천 가이드를 제공합니다. uv 패키지 매니저의 1.0 릴리스 소식도 함께 전합니다.",
        "content": """# FastAPI vs Django: 2026년 선택 가이드

## 언제 Django를 선택할까?
- 풀스택 웹 애플리케이션
- 관리자 패널이 필요한 프로젝트
- ORM 기반의 복잡한 데이터 모델링

## 언제 FastAPI를 선택할까?
- 마이크로서비스 아키텍처
- 고성능 API 서버
- 실시간 WebSocket 애플리케이션

---

# uv 1.0 릴리스

Astral의 uv가 드디어 1.0을 릴리스했습니다. pip 대비 10-100배 빠른 패키지 설치 속도를 자랑하며, 이제 프로덕션 환경에서도 안심하고 사용할 수 있습니다.

```bash
uv pip install django fastapi uvicorn
```

---

# SQLAlchemy 2.2 릴리스

새로운 `write_only` 관계 로딩 전략과 개선된 타입 힌트 지원이 추가되었습니다.
""",
        "tags": ["Python", "Django", "FastAPI", "Database"],
        "published_at": date(2026, 2, 1),
        "is_featured": False,
    },
    {
        "title": "[PyNews] 2026-01 - 2026년 파이썬 백엔드 트렌드 전망",
        "slug": "pynews-2026-01",
        "summary": "새해를 맞아 2026년 파이썬 백엔드 개발 트렌드를 전망합니다. AI 통합 API 개발, 서버리스 배포 패턴, 그리고 Rust 기반 Python 도구 생태계의 성장을 분석합니다.",
        "content": """# 2026년 파이썬 백엔드 트렌드 전망

## 1. AI 통합 API 개발
LLM을 활용한 API 개발이 보편화되고 있습니다. LangChain, LlamaIndex 등의 프레임워크와 Django/FastAPI의 통합 패턴이 표준화되고 있습니다.

## 2. Rust 기반 Python 도구의 부상
- **uv**: 초고속 패키지 매니저
- **Ruff**: 초고속 린터/포매터
- **Pydantic v3**: Rust 코어 기반 검증

## 3. 서버리스 & 컨테이너
AWS Lambda, Google Cloud Run 등에서의 Python 배포 패턴이 더욱 성숙해지고 있습니다.

## 4. 타입 안전성 강화
`mypy`, `pyright` 등 타입 체커의 발전으로 대규모 Python 프로젝트에서의 타입 안전성이 크게 향상되었습니다.
""",
        "tags": ["Python", "AI/ML", "DevOps"],
        "published_at": date(2026, 1, 1),
        "is_featured": False,
    },
    {
        "title": "[PyNews] 2025-12 - pytest 9.0과 테스트 전략 가이드",
        "slug": "pynews-2025-12",
        "summary": "pytest 9.0의 새로운 기능과 함께, 파이썬 백엔드 프로젝트에서의 효과적인 테스트 전략을 소개합니다. Fixture 스코프 관리, 병렬 테스트 실행, 그리고 통합 테스트 패턴을 다룹니다.",
        "content": """# pytest 9.0 릴리스

## 새로운 기능
- 개선된 assertion 리라이팅 엔진
- 네이티브 async fixture 지원
- 새로운 `--collect-only` 출력 형식

## 효과적인 테스트 전략

### 테스트 피라미드
1. **단위 테스트** (70%): 비즈니스 로직 검증
2. **통합 테스트** (20%): API 엔드포인트, DB 연동
3. **E2E 테스트** (10%): 전체 워크플로우 검증

```python
@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

async def test_create_post(async_client):
    response = await async_client.post("/api/posts/", json={"title": "Test"})
    assert response.status_code == 201
```
""",
        "tags": ["Python", "Testing"],
        "published_at": date(2025, 12, 1),
        "is_featured": False,
    },
    {
        "title": "[PyNews] 2025-11 - PostgreSQL + Django 성능 최적화 실전 가이드",
        "slug": "pynews-2025-11",
        "summary": "Django ORM과 PostgreSQL을 함께 사용할 때의 성능 최적화 기법을 실전 예제와 함께 소개합니다. 인덱스 전략, N+1 쿼리 해결, 그리고 커넥션 풀링 설정법을 다룹니다.",
        "content": """# PostgreSQL + Django 성능 최적화

## N+1 쿼리 문제 해결

```python
# Bad - N+1 쿼리 발생
posts = Post.objects.all()
for post in posts:
    print(post.author.name)  # 매번 추가 쿼리

# Good - select_related 사용
posts = Post.objects.select_related('author').all()
```

## 인덱스 전략
- `db_index=True`를 자주 검색하는 필드에 적용
- 복합 인덱스는 `Meta.indexes`에서 정의
- `EXPLAIN ANALYZE`로 쿼리 플랜 분석

## 커넥션 풀링
`django-db-connection-pool` 또는 PgBouncer를 활용한 커넥션 풀링으로 동시 접속 처리 능력을 향상시킬 수 있습니다.
""",
        "tags": ["Django", "Database"],
        "published_at": date(2025, 11, 1),
        "is_featured": False,
    },
]

for post_data in posts:
    tag_names = post_data.pop("tags")
    post, created = Post.objects.get_or_create(
        slug=post_data["slug"],
        defaults=post_data,
    )
    if created:
        for tag_name in tag_names:
            post.tags.add(tags[tag_name])
        print(f"Created: {post.title}")
    else:
        print(f"Already exists: {post.title}")

print("\nDone! Sample data seeded.")
