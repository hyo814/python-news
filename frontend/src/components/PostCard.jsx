import { Link } from 'react-router-dom';

export default function PostCard({ post }) {
  return (
    <article className="py-6 border-b border-gray-200 last:border-b-0 transition-transform hover:translate-x-1">
      <div className="flex items-center gap-3 mb-2 text-xs text-gray-500">
        <span className="font-medium">{post.published_at}</span>
        <span>·</span>
        <span>{post.author}</span>
        {post.source_type === 'crawled' && post.source_url && (
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
      <h3 className="text-lg font-bold mb-2 leading-snug">
        <Link to={`/post/${post.slug}`} className="text-gray-900 hover:text-primary transition-colors">
          {post.title}
        </Link>
      </h3>
      <p className="text-sm text-gray-500 leading-relaxed line-clamp-2">
        {post.summary}
      </p>
      <div className="flex gap-1.5 flex-wrap mt-3">
        {post.tags.map(tag => (
          <span
            key={tag.id}
            className="inline-block bg-gray-100 text-primary text-xs font-medium px-2.5 py-0.5 rounded-full border border-gray-200"
          >
            {tag.name}
          </span>
        ))}
      </div>
    </article>
  );
}
