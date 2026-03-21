import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchPosts } from '../api';
import PostCard from '../components/PostCard';
import SubscribeForm from '../components/SubscribeForm';

export default function Home() {
  const [editorial, setEditorial] = useState([]);
  const [crawled, setCrawled] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetchPosts('editorial'),
      fetchPosts('crawled'),
    ]).then(([ed, cr]) => {
      setEditorial(ed);
      setCrawled(cr.slice(0, 5));
      setLoading(false);
    });
  }, []);

  if (loading) {
    return <div className="text-center py-20 text-gray-400 text-base">불러오는 중...</div>;
  }

  const featured = editorial.find(p => p.is_featured);
  const otherEditorial = editorial.filter(p => !p.is_featured);

  return (
    <>
      {/* 히어로 - 피처드 에디터 글 */}
      {featured && (
        <section className="bg-linear-to-br from-primary to-[#1a4971] text-white py-12">
          <div className="max-w-3xl mx-auto px-6 text-center">
            <span className="inline-block bg-accent text-primary px-4 py-1 rounded-full text-xs font-bold uppercase tracking-wide mb-4">
              Latest Issue
            </span>
            <h2 className="text-3xl font-bold mb-4 leading-snug max-sm:text-2xl">
              {featured.title}
            </h2>
            <p className="text-base text-white/80 max-w-xl mx-auto mb-6 leading-relaxed">
              {featured.summary}
            </p>
            <Link
              to={`/post/${featured.slug}`}
              className="inline-block bg-accent text-primary px-7 py-2.5 rounded-md font-bold text-sm hover:bg-accent-dark transition-colors"
            >
              읽어보기 →
            </Link>
          </div>
        </section>
      )}

      {/* 에디터 직접 작성 글 */}
      {otherEditorial.length > 0 && (
        <section className="py-12">
          <div className="max-w-3xl mx-auto px-6">
            <h2 className="text-xl font-bold mb-8 pb-3 border-b-2 border-gray-200 text-gray-900">
              에디터 픽
            </h2>
            {otherEditorial.map(post => (
              <PostCard key={post.id} post={post} />
            ))}
          </div>
        </section>
      )}

      {/* 크롤링 최신 소식 */}
      {crawled.length > 0 && (
        <section className="py-12 bg-gray-50">
          <div className="max-w-3xl mx-auto px-6">
            <div className="flex items-center justify-between mb-8 pb-3 border-b-2 border-gray-200">
              <h2 className="text-xl font-bold text-gray-900">
                커뮤니티 소식
              </h2>
              <Link to="/archive" className="text-sm text-primary hover:text-primary-light font-medium">
                전체 보기 →
              </Link>
            </div>
            {crawled.map(post => (
              <PostCard key={post.id} post={post} />
            ))}
          </div>
        </section>
      )}

      {/* 구독 폼 */}
      <SubscribeForm />
    </>
  );
}
