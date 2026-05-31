import { Search, Settings, RefreshCw } from 'lucide-react';

interface NavbarProps {
  onSearchOpen: () => void;
  onSettingsOpen: () => void;
  onRefresh: () => void;
}

export default function Navbar({ onSearchOpen, onSettingsOpen, onRefresh }: NavbarProps) {
  return (
    <nav 
      className="fixed top-0 left-0 right-0 h-12 flex items-center justify-between px-6 z-50 transition-all duration-300"
      style={{
        backgroundColor: 'rgba(245, 243, 239, 0.92)',
        backdropFilter: 'blur(8px)',
        borderBottom: '1px solid var(--border-light)',
      }}
    >
      <div className="flex items-center gap-2">
        <span 
          className="font-display text-lg font-normal tracking-tight"
          style={{ color: 'var(--text-primary)' }}
        >
          HN Zen
        </span>
      </div>
      
      <div className="flex items-center gap-3">
        <button
          onClick={onSearchOpen}
          className="p-2 rounded-lg transition-colors hover:bg-black/5"
          style={{ color: 'var(--text-secondary)' }}
          title="Search (/)"
        >
          <Search size={16} />
        </button>
        <button
          onClick={onRefresh}
          className="p-2 rounded-lg transition-colors hover:bg-black/5"
          style={{ color: 'var(--text-secondary)' }}
          title="Refresh"
        >
          <RefreshCw size={16} />
        </button>
        <button
          onClick={onSettingsOpen}
          className="p-2 rounded-lg transition-colors hover:bg-black/5"
          style={{ color: 'var(--text-secondary)' }}
          title="Settings"
        >
          <Settings size={16} />
        </button>
      </div>
    </nav>
  );
}
