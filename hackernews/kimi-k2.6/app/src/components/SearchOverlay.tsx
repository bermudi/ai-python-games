import { useEffect, useRef, useState } from 'react';
import { X, Search } from 'lucide-react';

interface SearchOverlayProps {
  isOpen: boolean;
  onClose: () => void;
  searchQuery: string;
  onSearchChange: (query: string) => void;
}

export default function SearchOverlay({ isOpen, onClose, searchQuery, onSearchChange }: SearchOverlayProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [localQuery, setLocalQuery] = useState(searchQuery);
  
  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus();
    }
  }, [isOpen]);
  
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    
    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown);
      return () => document.removeEventListener('keydown', handleKeyDown);
    }
  }, [isOpen, onClose]);
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearchChange(localQuery);
    onClose();
  };
  
  const handleClear = () => {
    setLocalQuery('');
    onSearchChange('');
    inputRef.current?.focus();
  };

  if (!isOpen) return null;

  return (
    <div 
      className="fixed inset-0 z-[100] flex flex-col items-center pt-[20vh]"
      style={{
        backgroundColor: 'var(--canvas)',
        animation: 'fadeIn 0.2s ease',
      }}
    >
      {/* Close Button */}
      <button
        onClick={onClose}
        className="absolute top-4 right-4 p-2 rounded-lg transition-colors hover:bg-black/5"
        style={{ color: 'var(--text-secondary)' }}
      >
        <X size={20} />
      </button>
      
      {/* Search Input */}
      <form onSubmit={handleSubmit} className="w-full max-w-[600px] px-6">
        <div className="relative">
          <Search 
            size={20} 
            className="absolute left-0 top-1/2 -translate-y-1/2"
            style={{ color: 'var(--text-muted)' }}
          />
          <input
            ref={inputRef}
            type="text"
            value={localQuery}
            onChange={(e) => setLocalQuery(e.target.value)}
            placeholder="Search stories..."
            className="w-full bg-transparent font-display font-normal outline-none"
            style={{
              fontSize: 32,
              color: 'var(--text-primary)',
              paddingLeft: 36,
              paddingBottom: 12,
              borderBottom: '2px solid var(--border)',
            }}
          />
          {localQuery && (
            <button
              type="button"
              onClick={handleClear}
              className="absolute right-0 top-1/2 -translate-y-1/2 p-1 rounded transition-colors hover:bg-black/5"
              style={{ color: 'var(--text-muted)' }}
            >
              <X size={16} />
            </button>
          )}
        </div>
        
        {/* Hint */}
        <p 
          className="mt-4 font-body text-center"
          style={{ fontSize: 12, color: 'var(--text-muted)' }}
        >
          Press Enter to search · Escape to close
        </p>
      </form>
    </div>
  );
}
