#!/bin/bash
# 매주 월요일 오전 9시에 크롤링 실행
# 사용법: bash setup_cron.sh

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$PROJECT_DIR/venv/bin/python"
MANAGE="$PROJECT_DIR/manage.py"
LOG="$PROJECT_DIR/crawl.log"

CRON_CMD="0 9 * * 1 cd $PROJECT_DIR && $PYTHON $MANAGE crawl_news --days=7 >> $LOG 2>&1"

# 기존 크론에 이미 등록되어 있는지 확인
if crontab -l 2>/dev/null | grep -q "crawl_news"; then
    echo "이미 등록된 크론 작업이 있습니다."
    crontab -l | grep "crawl_news"
else
    (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
    echo "크론 작업이 등록되었습니다:"
    echo "$CRON_CMD"
fi

echo ""
echo "현재 크론 목록:"
crontab -l
