import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import { fetchPost } from '../api';

export default function PostDetail() {
  const { slug } = useParams();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPost(slug).then(data => {
      setPost(data);
      setLoading(false);
    });
  }, [slug]);

  if (loading) {
    return <div className="text-center py-20 text-gray-400 text-base">불러오는 중...</div>;
  }

  return (
    <section className="py-12 pb-16">
      <div className="max-w-3xl mx-auto px-6">
        <Link to="/" className="inline-flex items-center gap-1.5 text-sm text-gray-400 hover:text-primary mb-6">
          ← 목록으로
        </Link>

        <div className="mb-10 pb-6 border-b-2 border-gray-200">
          <div className="flex items-center gap-2 flex-wrap mb-3">
            {post.source_type === 'editorial' && (
              <span className="inline-block bg-accent text-primary text-xs font-bold px-2.5 py-0.5 rounded-full">
                에디터 픽
              </span>
            )}
            {post.tags.map(tag => (
              <span
                key={tag.id}
                className="inline-block bg-gray-100 text-primary text-xs font-medium px-2.5 py-0.5 rounded-full border border-gray-200"
              >
                {tag.name}
              </span>
            ))}
          </div>
          <h1 className="text-3xl font-bold leading-snug mb-4 max-sm:text-2xl">
            {post.title}
          </h1>
          <div className="flex items-center gap-4 text-gray-500 text-sm">
            <span>{post.author}</span>
            <span>·</span>
            <span>{post.published_at}</span>
            {post.source_url && (
              <>
                <span>·</span>
                <a
                  href={post.source_url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-primary hover:underline"
                >
                  원본 링크 ↗
                </a>
              </>
            )}
          </div>
        </div>

        <div className="prose text-base leading-relaxed">
          <ReactMarkdown>{post.content}</ReactMarkdown>
        </div>
      </div>
    </section>
  );
}
