import { useState, useRef, useEffect } from 'react';
import { ExternalLink, Eye, Bell, BellOff } from 'lucide-react';
import type { HNStory } from '@/types/hn';
import { useNavigate } from 'react-router';

interface StoryRowProps {
  story: HNStory;
  index: number;
  onFollow: (storyId: number) => void;
  timeAgo: (timestamp: number) => string;
  isVisible: boolean;
}

export default function StoryRow({ story, index, onFollow, timeAgo, isVisible }: StoryRowProps) {
  const [hovered, setHovered] = useState(false);
  const [contextMenu, setContextMenu] = useState<{ x: number; y: number } | null>(null);
  const rowRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  
  const handleClick = () => {
    navigate(`/story/${story.id}`);
  };
  
  const handleTitleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (story.url) {
      window.open(story.url, '_blank');
    }
  };
  
  const handleContextMenu = (e: React.MouseEvent) => {
    e.preventDefault();
    setContextMenu({ x: e.clientX, y: e.clientY });
  };
  
  const handleMarkVisited = () => {
    // Handled by navigation
    setContextMenu(null);
  };
  
  const handleFollow = () => {
    onFollow(story.id);
    setContextMenu(null);
  };
  
  useEffect(() => {
    const handleClickOutside = () => setContextMenu(null);
    if (contextMenu) {
      document.addEventListener('click', handleClickOutside);
      return () => document.removeEventListener('click', handleClickOutside);
    }
  }, [contextMenu]);
  
  const commentCount = story.descendants || 0;
  const isVisited = story.visited;
  
  return (
    <>
      <div
        ref={rowRef}
        className="story-row relative flex items-start gap-4 px-6 py-5 cursor-pointer select-none"
        style={{
          borderBottom: '1px solid var(--border-light)',
          opacity: isVisible ? 1 : 0,
          transform: isVisible ? 'translateY(0)' : 'translateY(8px)',
          transition: `opacity 0.4s ease ${index * 0.03}s, transform 0.4s ease ${index * 0.03}s`,
        }}
        onClick={handleClick}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
        onContextMenu={handleContextMenu}
      >
        {/* Score Badge */}
        <div className="flex-shrink-0 w-12 flex justify-center pt-0.5">
          <span 
            className="score-badge"
            style={{
              opacity: isVisited ? 0.6 : 1,
            }}
          >
            {story.score || 0}
          </span>
        </div>
        
        {/* Content */}
        <div className="flex-1 min-w-0">
          {/* Title */}
          <div className="flex items-start gap-2">
            <h3 
              className="font-body font-medium leading-relaxed cursor-pointer"
              style={{ 
                fontSize: 15,
                lineHeight: 1.45,
                color: isVisited ? 'var(--visited)' : 'var(--text-primary)',
                transition: 'color 0.15s ease',
              }}
              onClick={handleTitleClick}
            >
              {story.title}
            </h3>
            {hovered && story.url && (
              <ExternalLink 
                size={10} 
                className="flex-shrink-0 mt-1.5"
                style={{ color: 'var(--text-muted)' }}
              />
            )}
          </div>
          
          {/* Domain */}
          <p 
            className="mt-1 font-body uppercase tracking-wider"
            style={{ 
              fontSize: 11, 
              color: 'var(--text-muted)',
              letterSpacing: '0.5px',
            }}
          >
            {story.domain}
          </p>
          
          {/* Meta */}
          <div className="flex items-center gap-2 mt-1.5">
            <span 
              className="font-body"
              style={{ fontSize: 12, color: 'var(--text-secondary)' }}
            >
              by {story.by}
            </span>
            <span style={{ color: 'var(--text-muted)' }}>·</span>
            <span 
              className="font-body"
              style={{ fontSize: 12, color: 'var(--text-secondary)' }}
            >
              {story.time ? timeAgo(story.time) : 'unknown'}
            </span>
            <span style={{ color: 'var(--text-muted)' }}>·</span>
            <span 
              className="font-body"
              style={{ fontSize: 12, color: 'var(--text-secondary)' }}
            >
              {commentCount} comment{commentCount !== 1 ? 's' : ''}
            </span>
            {isVisited && (
              <>
                <span style={{ color: 'var(--text-muted)' }}>·</span>
                <Eye size={12} style={{ color: 'var(--visited)' }} />
              </>
            )}
            {story.following && (
              <>
                <span style={{ color: 'var(--text-muted)' }}>·</span>
                <Bell size={12} style={{ color: 'var(--accent)' }} />
              </>
            )}
          </div>
        </div>
        
        {/* Follow button - visible on hover */}
        {hovered && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onFollow(story.id);
            }}
            className="flex-shrink-0 p-1.5 rounded-md transition-colors"
            style={{ 
              color: story.following ? 'var(--accent)' : 'var(--text-muted)',
            }}
            title={story.following ? 'Unfollow thread' : 'Follow thread'}
          >
            {story.following ? <Bell size={14} /> : <BellOff size={14} />}
          </button>
        )}
      </div>
      
      {/* Context Menu */}
      {contextMenu && (
        <div
          className="fixed z-50 py-1 rounded-lg shadow-lg border"
          style={{
            left: contextMenu.x,
            top: contextMenu.y,
            backgroundColor: 'var(--surface)',
            borderColor: 'var(--border)',
            minWidth: 180,
          }}
        >
          <button
            onClick={handleMarkVisited}
            className="w-full flex items-center gap-2 px-3 py-2 text-left font-body text-sm transition-colors hover:bg-black/5"
            style={{ color: 'var(--text-secondary)' }}
          >
            <Eye size={14} />
            {isVisited ? 'Mark as unvisited' : 'Mark as visited'}
          </button>
          <button
            onClick={handleFollow}
            className="w-full flex items-center gap-2 px-3 py-2 text-left font-body text-sm transition-colors hover:bg-black/5"
            style={{ color: 'var(--text-secondary)' }}
          >
            {story.following ? <Bell size={14} /> : <BellOff size={14} />}
            {story.following ? 'Unfollow thread' : 'Follow thread'}
          </button>
          <div className="my-1 border-t" style={{ borderColor: 'var(--border-light)' }} />
          <button
            onClick={() => {
              if (story.url) window.open(story.url, '_blank');
              setContextMenu(null);
            }}
            className="w-full flex items-center gap-2 px-3 py-2 text-left font-body text-sm transition-colors hover:bg-black/5"
            style={{ color: 'var(--text-secondary)' }}
          >
            <ExternalLink size={14} />
            Open in new tab
          </button>
        </div>
      )}
    </>
  );
}
