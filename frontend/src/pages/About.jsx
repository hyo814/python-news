export default function About() {
  return (
    <section className="py-12 pb-16">
      <div className="max-w-3xl mx-auto px-6">
        <h1 className="text-3xl font-bold mb-6">About PyNews</h1>
        <p className="mb-4 leading-relaxed text-base">
          <strong className="text-gray-900">PyNews</strong>는 파이썬 백엔드 개발자를 위한 월간 뉴스레터입니다.
          Django, FastAPI, Flask 등 파이썬 웹 프레임워크와 백엔드 개발 생태계의
          최신 소식을 큐레이션하여 전달합니다.
        </p>
        <p className="mb-4 leading-relaxed text-base">
          매주 월요일 RSS 피드에서 자동으로 최신 소식을 수집하며, 다음과 같은 주제를 다룹니다:
        </p>
        <ul className="list-disc ml-6 mb-4 space-y-2 text-base">
          <li>파이썬 및 주요 프레임워크 릴리스 소식</li>
          <li>백엔드 아키텍처 및 설계 패턴</li>
          <li>데이터베이스 및 성능 최적화</li>
          <li>테스트 전략 및 DevOps</li>
          <li>AI/ML 통합 백엔드 개발</li>
        </ul>
        <p className="leading-relaxed text-base">
          FE News(<a href="https://fenews.substack.com/" target="_blank" rel="noreferrer" className="text-primary hover:text-primary-light underline">fenews.substack.com</a>)에서
          영감을 받아 시작된 프로젝트입니다.
        </p>
      </div>
    </section>
  );
}
