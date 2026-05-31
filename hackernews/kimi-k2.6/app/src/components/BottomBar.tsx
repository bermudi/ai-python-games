import { useState, useEffect, useRef } from 'react';
import { Eye, EyeOff } from 'lucide-react';
import { Switch } from '@/components/ui/switch';
import type { StoryType } from '@/types/hn';

interface BottomBarProps {
  storyType: StoryType;
  onStoryTypeChange: (type: StoryType) => void;
  hideVisited: boolean;
  onHideVisitedChange: (value: boolean) => void;
  page: number;
}

const storyTypes: { value: StoryType; label: string }[] = [
  { value: 'top', label: 'Top' },
  { value: 'new', label: 'New' },
  { value: 'best', label: 'Best' },
];

export default function BottomBar({
  storyType,
  onStoryTypeChange,
  hideVisited,
  onHideVisitedChange,
  page,
}: BottomBarProps) {
  const [keyboardHint, setKeyboardHint] = useState(false);
  const hintTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
      
      if (e.key === 'h' || e.key === 'H') {
        onHideVisitedChange(!hideVisited);
        showHint(`Hide visited: ${!hideVisited ? 'ON' : 'OFF'}`);
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [hideVisited, onHideVisitedChange]);
  
  const showHint = (_text: string) => {
    setKeyboardHint(true);
    if (hintTimer.current) clearTimeout(hintTimer.current);
    hintTimer.current = setTimeout(() => setKeyboardHint(false), 1500);
  };

  return (
    <>
      <div 
        className="fixed bottom-0 left-0 right-0 z-40"
        style={{
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(12px)',
          borderTop: '1px solid var(--border)',
        }}
      >
        <div className="max-w-[680px] mx-auto px-6 py-3 flex items-center justify-between">
          {/* Story Type Pills */}
          <div className="flex items-center gap-1">
            {storyTypes.map(type => (
              <button
                key={type.value}
                onClick={() => onStoryTypeChange(type.value)}
                className="action-pill"
                style={{
                  backgroundColor: storyType === type.value ? 'var(--badge-bg)' : 'transparent',
                  color: storyType === type.value ? 'var(--badge-text)' : 'var(--text-secondary)',
                  borderColor: storyType === type.value ? 'var(--badge-bg)' : 'var(--border)',
                  padding: '6px 14px',
                  fontSize: 12,
                  fontWeight: 500,
                }}
              >
                {type.label}
              </button>
            ))}
          </div>
          
          {/* Hide Visited Toggle */}
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-1.5">
              {hideVisited ? (
                <EyeOff size={14} style={{ color: 'var(--text-muted)' }} />
              ) : (
                <Eye size={14} style={{ color: 'var(--text-muted)' }} />
              )}
              <span 
                className="font-body hidden sm:inline"
                style={{ fontSize: 12, color: 'var(--text-secondary)' }}
              >
                Hide Visited
              </span>
            </div>
            <Switch
              checked={hideVisited}
              onCheckedChange={onHideVisitedChange}
              className="data-[state=checked]:bg-[var(--accent)]"
            />
          </div>
          
          {/* Page Indicator */}
          <span 
            className="font-body hidden sm:block"
            style={{ fontSize: 12, color: 'var(--text-muted)' }}
          >
            Page {page + 1}
          </span>
        </div>
      </div>
      
      {/* Keyboard Hint Toast */}
      {keyboardHint && (
        <div 
          className="fixed bottom-20 left-1/2 -translate-x-1/2 z-50 px-4 py-2 rounded-lg font-body text-sm transition-opacity"
          style={{
            backgroundColor: 'var(--badge-bg)',
            color: 'var(--badge-text)',
          }}
        >
          Hide visited: {hideVisited ? 'ON' : 'OFF'}
        </div>
      )}
    </>
  );
}
