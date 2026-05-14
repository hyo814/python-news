import { useEffect, useState } from 'react';

export default function LoadingState() {
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setElapsed(e => e + 1), 1000);
    return () => clearInterval(id);
  }, []);

  let message = '불러오는 중...';
  if (elapsed >= 10 && elapsed < 40) {
    message = '서버가 깨어나는 중이에요 (Render 무료 플랜, 최대 1분 정도 소요)';
  } else if (elapsed >= 40) {
    message = '조금만 더 기다려주세요...';
  }

  return (
    <div className="text-center py-20 text-gray-400 text-base">
      <div className="inline-block w-6 h-6 border-2 border-gray-200 border-t-primary rounded-full animate-spin mb-3" />
      <p>{message}</p>
      {elapsed >= 10 && (
        <p className="text-xs text-gray-300 mt-2">{elapsed}초 경과</p>
      )}
    </div>
  );
}