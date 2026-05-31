import { useState } from 'react';
import { X, Moon, Sun, Monitor, Trash2, AlertTriangle } from 'lucide-react';

type ThemeMode = 'light' | 'dark' | 'auto';

interface SettingsPanelProps {
  isOpen: boolean;
  onClose: () => void;
  darkMode: boolean;
  onDarkModeChange: (value: boolean) => void;
  onClearVisited: () => void;
  onClearFollowed: () => void;
}

export default function SettingsPanel({
  isOpen,
  onClose,
  darkMode: _darkMode,
  onDarkModeChange,
  onClearVisited,
  onClearFollowed,
}: SettingsPanelProps) {
  const [themeMode, setThemeMode] = useState<ThemeMode>('light');
  const [showClearVisitedConfirm, setShowClearVisitedConfirm] = useState(false);
  const [showClearFollowedConfirm, setShowClearFollowedConfirm] = useState(false);

  const handleThemeChange = (mode: ThemeMode) => {
    setThemeMode(mode);
    if (mode === 'light') {
      onDarkModeChange(false);
    } else if (mode === 'dark') {
      onDarkModeChange(true);
    } else {
      // Auto - use system preference
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      onDarkModeChange(prefersDark);
    }
  };

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div 
        className="fixed inset-0 z-[90] bg-black/20 transition-opacity"
        onClick={onClose}
      />
      
      {/* Panel */}
      <div 
        className="fixed top-0 right-0 bottom-0 w-[360px] z-[100] overflow-y-auto"
        style={{
          backgroundColor: 'var(--surface)',
          boxShadow: '-4px 0 24px rgba(0,0,0,0.08)',
          animation: 'slideIn 0.3s ease',
        }}
      >
        {/* Header */}
        <div 
          className="flex items-center justify-between px-6 py-4"
          style={{ borderBottom: '1px solid var(--border-light)' }}
        >
          <h2 
            className="font-display font-normal"
            style={{ fontSize: 20, color: 'var(--text-primary)' }}
          >
            Settings
          </h2>
          <button
            onClick={onClose}
            className="p-2 rounded-lg transition-colors hover:bg-black/5"
            style={{ color: 'var(--text-secondary)' }}
          >
            <X size={18} />
          </button>
        </div>
        
        {/* Content */}
        <div className="px-6 py-6 space-y-8">
          
          {/* Theme */}
          <div>
            <h3 
              className="font-body font-medium mb-3"
              style={{ fontSize: 13, color: 'var(--text-primary)', textTransform: 'uppercase', letterSpacing: '0.5px' }}
            >
              Theme
            </h3>
            <div className="flex gap-2">
              <button
                onClick={() => handleThemeChange('light')}
                className="flex items-center gap-2 px-4 py-2.5 rounded-lg border transition-all"
                style={{
                  borderColor: themeMode === 'light' ? 'var(--accent)' : 'var(--border)',
                  backgroundColor: themeMode === 'light' ? 'var(--accent-soft)' : 'transparent',
                  color: themeMode === 'light' ? 'var(--accent)' : 'var(--text-secondary)',
                }}
              >
                <Sun size={16} />
                <span className="font-body text-sm">Light</span>
              </button>
              <button
                onClick={() => handleThemeChange('dark')}
                className="flex items-center gap-2 px-4 py-2.5 rounded-lg border transition-all"
                style={{
                  borderColor: themeMode === 'dark' ? 'var(--accent)' : 'var(--border)',
                  backgroundColor: themeMode === 'dark' ? 'var(--accent-soft)' : 'transparent',
                  color: themeMode === 'dark' ? 'var(--accent)' : 'var(--text-secondary)',
                }}
              >
                <Moon size={16} />
                <span className="font-body text-sm">Dark</span>
              </button>
              <button
                onClick={() => handleThemeChange('auto')}
                className="flex items-center gap-2 px-4 py-2.5 rounded-lg border transition-all"
                style={{
                  borderColor: themeMode === 'auto' ? 'var(--accent)' : 'var(--border)',
                  backgroundColor: themeMode === 'auto' ? 'var(--accent-soft)' : 'transparent',
                  color: themeMode === 'auto' ? 'var(--accent)' : 'var(--text-secondary)',
                }}
              >
                <Monitor size={16} />
                <span className="font-body text-sm">Auto</span>
              </button>
            </div>
          </div>
          
          {/* Data Management */}
          <div>
            <h3 
              className="font-body font-medium mb-3"
              style={{ fontSize: 13, color: 'var(--text-primary)', textTransform: 'uppercase', letterSpacing: '0.5px' }}
            >
              Data
            </h3>
            <div className="space-y-3">
              {/* Clear Visited */}
              <div 
                className="p-4 rounded-lg border"
                style={{ borderColor: 'var(--border-light)' }}
              >
                {!showClearVisitedConfirm ? (
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-body text-sm font-medium" style={{ color: 'var(--text-primary)' }}>
                        Clear visited stories
                      </p>
                      <p className="font-body text-xs mt-0.5" style={{ color: 'var(--text-muted)' }}>
                        Remove all visited story markers
                      </p>
                    </div>
                    <button
                      onClick={() => setShowClearVisitedConfirm(true)}
                      className="p-2 rounded-lg transition-colors hover:bg-red-50"
                      style={{ color: '#E53E3E' }}
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                ) : (
                  <div className="space-y-3">
                    <div className="flex items-center gap-2" style={{ color: '#E53E3E' }}>
                      <AlertTriangle size={16} />
                      <p className="font-body text-sm font-medium">Are you sure?</p>
                    </div>
                    <p className="font-body text-xs" style={{ color: 'var(--text-muted)' }}>
                      This will clear all visited story markers. This cannot be undone.
                    </p>
                    <div className="flex gap-2">
                      <button
                        onClick={() => {
                          onClearVisited();
                          setShowClearVisitedConfirm(false);
                        }}
                        className="px-4 py-2 rounded-lg font-body text-sm font-medium text-white"
                        style={{ backgroundColor: '#E53E3E' }}
                      >
                        Clear
                      </button>
                      <button
                        onClick={() => setShowClearVisitedConfirm(false)}
                        className="px-4 py-2 rounded-lg font-body text-sm"
                        style={{ color: 'var(--text-secondary)', border: '1px solid var(--border)' }}
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                )}
              </div>
              
              {/* Clear Followed */}
              <div 
                className="p-4 rounded-lg border"
                style={{ borderColor: 'var(--border-light)' }}
              >
                {!showClearFollowedConfirm ? (
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-body text-sm font-medium" style={{ color: 'var(--text-primary)' }}>
                        Clear followed threads
                      </p>
                      <p className="font-body text-xs mt-0.5" style={{ color: 'var(--text-muted)' }}>
                        Unfollow all threads
                      </p>
                    </div>
                    <button
                      onClick={() => setShowClearFollowedConfirm(true)}
                      className="p-2 rounded-lg transition-colors hover:bg-red-50"
                      style={{ color: '#E53E3E' }}
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                ) : (
                  <div className="space-y-3">
                    <div className="flex items-center gap-2" style={{ color: '#E53E3E' }}>
                      <AlertTriangle size={16} />
                      <p className="font-body text-sm font-medium">Are you sure?</p>
                    </div>
                    <p className="font-body text-xs" style={{ color: 'var(--text-muted)' }}>
                      This will unfollow all threads. This cannot be undone.
                    </p>
                    <div className="flex gap-2">
                      <button
                        onClick={() => {
                          onClearFollowed();
                          setShowClearFollowedConfirm(false);
                        }}
                        className="px-4 py-2 rounded-lg font-body text-sm font-medium text-white"
                        style={{ backgroundColor: '#E53E3E' }}
                      >
                        Unfollow All
                      </button>
                      <button
                        onClick={() => setShowClearFollowedConfirm(false)}
                        className="px-4 py-2 rounded-lg font-body text-sm"
                        style={{ color: 'var(--text-secondary)', border: '1px solid var(--border)' }}
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
          
          {/* Keyboard Shortcuts */}
          <div>
            <h3 
              className="font-body font-medium mb-3"
              style={{ fontSize: 13, color: 'var(--text-primary)', textTransform: 'uppercase', letterSpacing: '0.5px' }}
            >
              Keyboard Shortcuts
            </h3>
            <div className="space-y-2">
              {[
                { key: '/', desc: 'Open search' },
                { key: 'Esc', desc: 'Close / Go back' },
                { key: 'j', desc: 'Next story' },
                { key: 'k', desc: 'Previous story' },
                { key: 'h', desc: 'Toggle hide visited' },
              ].map(({ key, desc }) => (
                <div key={key} className="flex items-center justify-between py-1">
                  <span className="font-body text-sm" style={{ color: 'var(--text-secondary)' }}>
                    {desc}
                  </span>
                  <kbd 
                    className="px-2 py-1 rounded font-body text-xs font-medium"
                    style={{
                      backgroundColor: 'var(--surface-hover)',
                      color: 'var(--text-secondary)',
                      border: '1px solid var(--border)',
                    }}
                  >
                    {key}
                  </kbd>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
