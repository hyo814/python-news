import { useState } from 'react';
import { subscribe } from '../api';

export default function SubscribeForm() {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState(null); // 'success' | 'error'
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await subscribe(email);
      setStatus('success');
      setMessage(data.message);
      setEmail('');
    } catch (err) {
      setStatus('error');
      setMessage(err.email?.[0] || '구독 중 오류가 발생했습니다.');
    }
  };

  return (
    <section className="bg-gray-50 border-t border-gray-200">
      <div className="max-w-3xl mx-auto px-6 py-12 text-center">
        <h2 className="text-xl font-bold text-gray-900 mb-2">
          뉴스레터 구독
        </h2>
        <p className="text-sm text-gray-500 mb-6">
          매주 월요일, 파이썬 백엔드 최신 소식을 이메일로 받아보세요.
        </p>

        <form onSubmit={handleSubmit} className="flex gap-2 max-w-md mx-auto max-sm:flex-col">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="이메일 주소를 입력하세요"
            required
            className="flex-1 px-4 py-2.5 rounded-lg border border-gray-300 text-sm
                       focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
          />
          <button
            type="submit"
            className="px-6 py-2.5 bg-primary text-white text-sm font-bold rounded-lg
                       hover:bg-primary-light transition-colors shrink-0"
          >
            구독하기
          </button>
        </form>

        {status && (
          <p className={`mt-4 text-sm ${status === 'success' ? 'text-green-600' : 'text-red-500'}`}>
            {message}
          </p>
        )}
      </div>
    </section>
  );
}
