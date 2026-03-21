# 🐍 PyNews - 파이썬 백엔드 개발 뉴스레터

[FE News](https://fenews.substack.com/)에서 영감을 받아 만든 **파이썬 백엔드 개발자를 위한 뉴스레터 플랫폼**입니다.
Django, FastAPI, Flask 등 파이썬 웹 생태계의 최신 소식을 자동 수집하고, 에디터가 직접 작성한 글과 함께 제공합니다.

## 기술 스택

| 영역 | 기술 |
|------|------|
| **Backend** | Django 6.0, Django REST Framework |
| **Frontend** | React 19, Tailwind CSS 4, Vite 8 |
| **Database** | SQLite |
| **크롤링** | feedparser, BeautifulSoup4 |
| **이메일** | Django Email (SMTP) |

## 프로젝트 구조

```
python-news/
├── config/                  # Django 프로젝트 설정
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── news/                    # 메인 앱
│   ├── models.py            # Post, Tag, Subscriber 모델
│   ├── serializers.py       # DRF 시리얼라이저
│   ├── views.py             # API 뷰 (목록, 상세, 구독)
│   ├── urls.py              # API 라우팅
│   ├── admin.py             # Django Admin 설정
│   └── management/commands/
│       ├── crawl_news.py    # RSS 크롤링 커맨드
│       └── send_newsletter.py  # 뉴스레터 발송 커맨드
├── frontend/                # React SPA
│   ├── src/
│   │   ├── components/      # Header, Footer, PostCard, SubscribeForm
│   │   ├── pages/           # Home, Archive, PostDetail, About
│   │   ├── api.js           # API 호출 함수
│   │   ├── App.jsx          # 라우터 설정
│   │   └── index.css        # Tailwind 진입점
│   ├── vite.config.js       # Vite + Tailwind 플러그인
│   └── index.html
├── seed_data.py             # 샘플 데이터 시딩
├── setup_cron.sh            # 크론 자동 등록 스크립트
├── requirements.txt
└── manage.py
```

## 개발 과정

### 1단계: Django REST API 구축

Django 프로젝트를 생성하고 `news` 앱에 핵심 모델을 설계했습니다.

- **Post** - 뉴스 글 (제목, 요약, Markdown 본문, 태그, 발행일)
- **Tag** - 분류 태그 (Python, Django, FastAPI, DevOps 등)
- **Subscriber** - 이메일 구독자 (UUID 토큰 기반 구독/해지)

`source_type` 필드로 **직접 작성(editorial)** 글과 **크롤링(crawled)** 글을 구분합니다.
Django Admin에서 글을 작성하면 editorial로, 크롤러가 수집하면 crawled로 자동 분류됩니다.

DRF로 REST API를 구성했습니다:

| 엔드포인트 | 설명 |
|-----------|------|
| `GET /api/posts/` | 전체 글 목록 (`?type=editorial\|crawled`, `?tag=slug` 필터) |
| `GET /api/posts/<slug>/` | 글 상세 |
| `GET /api/posts/featured/` | 피처드 글 |
| `GET /api/tags/` | 태그 목록 |
| `POST /api/subscribe/` | 이메일 구독 |
| `POST /api/unsubscribe/` | 구독 해지 |

### 2단계: RSS 크롤링 시스템

`feedparser`를 사용해 11개 RSS 소스에서 뉴스를 자동 수집하는 Django management command를 만들었습니다.

**영어 소스:**
- Python 공식 블로그, Django 공식 블로그
- Real Python, Planet Python, Python Weekly

**한국어 소스:**
- GeekNews, 44bits, NHN Cloud Meetup
- 우아한형제들 기술블로그, LINE Engineering, Toss Tech

한국어 소스는 파이썬/백엔드 관련 키워드(`python`, `django`, `fastapi`, `백엔드` 등)가 포함된 글만 필터링합니다.
수집된 글은 제목과 요약을 분석해 Django, FastAPI, Database, DevOps 등의 태그를 자동 부여합니다.

```bash
# 크롤링 실행 (최근 7일)
python manage.py crawl_news

# 최근 30일, 저장 없이 테스트
python manage.py crawl_news --days=30 --dry-run
```

### 3단계: 주간 스케줄링

`setup_cron.sh` 스크립트로 crontab에 등록하면 **매주 월요일 오전 9시**에 자동 크롤링됩니다.

```bash
bash setup_cron.sh
```

등록되는 크론:
```
0 9 * * 1 cd /path/to/project && venv/bin/python manage.py crawl_news --days=7 >> crawl.log 2>&1
```

### 4단계: React 프론트엔드

Vite로 React 프로젝트를 생성하고 Tailwind CSS 4를 `@tailwindcss/vite` 플러그인으로 통합했습니다.
Python 브랜드 컬러(파란색 `#306998`, 노란색 `#FFD43B`)를 커스텀 테마로 적용했습니다.

**페이지 구성:**

- **Home** - 히어로 배너(피처드 에디터 글) + 에디터 픽 + 커뮤니티 소식(최신 5개) + 구독 폼
- **Archive** - 전체 글 목록 + 태그 필터링
- **PostDetail** - Markdown 렌더링된 글 상세 (에디터 픽 뱃지, 원본 링크 표시)
- **About** - 프로젝트 소개

### 5단계: 이메일 구독

FE News처럼 이메일 구독 기능을 구현했습니다.

- Home 하단에 이메일 입력 폼 배치
- 중복 구독 방지 + 구독 해지(UUID 토큰 기반)
- `send_newsletter` 커맨드로 구독자에게 주간 뉴스레터 발송

```bash
# 뉴스레터 발송 (미리보기)
python manage.py send_newsletter --dry-run

# 실제 발송
python manage.py send_newsletter
```

개발 환경에서는 이메일이 콘솔에 출력되며, 프로덕션에서는 `config/settings.py`에서 SMTP를 설정하면 실제 발송됩니다.

## 시작하기

### 사전 요구사항

- Python 3.12+
- Node.js 20+

### 설치 및 실행

```bash
# 1. 클론
git clone <repo-url>
cd python-news

# 2. 백엔드 설정
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. DB 초기화 + 샘플 데이터
python manage.py migrate
python manage.py createsuperuser
python seed_data.py

# 4. 크롤링 실행
python manage.py crawl_news --days=30

# 5. 프론트엔드 설정
cd frontend
npm install
cd ..

# 6. 서버 실행 (터미널 2개)
python manage.py runserver          # http://localhost:8000
cd frontend && npm run dev          # http://localhost:5173
```

### 관리

- **Django Admin**: http://localhost:8000/admin - 글 작성, 구독자 관리
- **크롤링**: `python manage.py crawl_news`
- **뉴스레터 발송**: `python manage.py send_newsletter`
- **주간 자동화**: `bash setup_cron.sh`

## 프로덕션 이메일 설정

`config/settings.py`에서 이메일 백엔드를 SMTP로 변경합니다:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.SmtpEmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 라이선스

MIT
