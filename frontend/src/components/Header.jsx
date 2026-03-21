import { Link, useLocation } from 'react-router-dom';

export default function Header() {
  const { pathname } = useLocation();

  const navLink = (to, label) => (
    <Link
      to={to}
      className={`text-sm font-medium transition-colors ${
        pathname === to ? 'text-accent' : 'text-white/80 hover:text-accent'
      }`}
    >
      {label}
    </Link>
  );

  return (
    <header className="bg-primary border-b-4 border-accent">
      <div className="max-w-3xl mx-auto px-6 py-5 flex items-center justify-between max-sm:flex-col max-sm:gap-3">
        <Link to="/" className="flex items-center gap-3 text-white font-bold text-2xl">
          <span className="text-3xl">🐍</span>
          <div>
            PyNews
            <div className="text-xs font-normal text-white/70">
              파이썬 백엔드 개발 뉴스레터
            </div>
          </div>
        </Link>
        <nav className="flex gap-6">
          {navLink('/', 'Home')}
          {navLink('/archive', 'Archive')}
          {navLink('/about', 'About')}
        </nav>
      </div>
    </header>
  );
}
