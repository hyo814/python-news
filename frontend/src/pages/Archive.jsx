import { useEffect, useState } from 'react';
import { fetchPosts, fetchTags } from '../api';
import PostCard from '../components/PostCard';

export default function Archive() {
  const [posts, setPosts] = useState([]);
  const [tags, setTags] = useState([]);
  const [activeTag, setActiveTag] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([fetchPosts(), fetchTags()]).then(([p, t]) => {
      setPosts(p);
      setTags(t);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return <div className="text-center py-20 text-gray-400 text-base">불러오는 중...</div>;
  }

  const filtered = activeTag
    ? posts.filter(p => p.tags.some(t => t.slug === activeTag))
    : posts;

  return (
    <section className="py-12 pb-16">
      <div className="max-w-3xl mx-auto px-6">
        <h2 className="text-xl font-bold mb-6 pb-3 border-b-2 border-gray-200 text-gray-900">
          전체 아카이브
        </h2>

        {/* 태그 필터 */}
        <div className="flex gap-2 flex-wrap mb-8">
          <button
            onClick={() => setActiveTag(null)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              !activeTag
                ? 'bg-primary text-white border-primary'
                : 'bg-white text-gray-600 border-gray-300 hover:border-primary hover:text-primary'
            }`}
          >
            전체
          </button>
          {tags.map(tag => (
            <button
              key={tag.id}
              onClick={() => setActiveTag(tag.slug === activeTag ? null : tag.slug)}
              className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
                activeTag === tag.slug
                  ? 'bg-primary text-white border-primary'
                  : 'bg-white text-gray-600 border-gray-300 hover:border-primary hover:text-primary'
              }`}
            >
              {tag.name}
            </button>
          ))}
        </div>

        {/* 포스트 목록 */}
        <p className="text-sm text-gray-400 mb-4">{filtered.length}개의 글</p>
        {filtered.map(post => (
          <PostCard key={post.id} post={post} />
        ))}
        {filtered.length === 0 && (
          <p className="text-center py-12 text-gray-400">해당 태그의 글이 없습니다.</p>
        )}
      </div>
    </section>
  );
}
