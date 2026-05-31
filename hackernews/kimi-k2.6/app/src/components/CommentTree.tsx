import { useState } from 'react';
import { Minus, Plus } from 'lucide-react';
import type { HNComment } from '@/types/hn';

interface CommentTreeProps {
  comments: HNComment[];
  onToggleCollapse: (commentId: number) => void;
  timeAgo: (timestamp: number) => string;
  depth?: number;
}

function CommentNode({ 
  comment, 
  onToggleCollapse, 
  timeAgo,
  depth = 0,
}: {
  comment: HNComment;
  onToggleCollapse: (commentId: number) => void;
  timeAgo: (timestamp: number) => string;
  depth?: number;
}) {
  const isCollapsed = comment.collapsed;
  const replyCount = comment.children?.length || 0;
  const totalReplies = countAllReplies(comment);
  
  if (isCollapsed) {
    return (
      <div 
        className="py-2 cursor-pointer select-none"
        style={{ 
          paddingLeft: depth > 0 ? 24 : 0,
          borderLeft: depth > 0 ? '2px solid var(--border-light)' : 'none',
          marginLeft: depth > 0 ? 12 : 0,
        }}
        onClick={() => onToggleCollapse(comment.id)}
      >
        <div className="flex items-center gap-2">
          <button
            className="p-0.5 rounded transition-colors"
            style={{ color: 'var(--text-muted)' }}
          >
            <Plus size={12} />
          </button>
          <span 
            className="font-body font-semibold"
            style={{ fontSize: 12, color: 'var(--accent)' }}
          >
            {comment.by}
          </span>
          <span style={{ color: 'var(--text-muted)' }}>·</span>
          <span className="comment-meta">
            {comment.time ? timeAgo(comment.time) : 'unknown'}
          </span>
          <span style={{ color: 'var(--text-muted)' }}>·</span>
          <span 
            className="font-body"
            style={{ fontSize: 11, color: 'var(--text-muted)' }}
          >
            {totalReplies} repl{totalReplies === 1 ? 'y' : 'ies'}
          </span>
        </div>
      </div>
    );
  }
  
  return (
    <div 
      className="py-3"
      style={{ 
        paddingLeft: depth > 0 ? 24 : 0,
        borderLeft: depth > 0 ? '2px solid var(--border-light)' : 'none',
        marginLeft: depth > 0 ? 12 : 0,
      }}
      
    >
      {/* Comment Header */}
      <div className="flex items-center gap-2 mb-1.5">
        <button
          onClick={() => onToggleCollapse(comment.id)}
          className="p-0.5 rounded transition-colors"
          style={{ color: 'var(--text-muted)' }}
          title="Collapse"
        >
          <Minus size={12} />
        </button>
        <span 
          className="font-body font-semibold"
          style={{ fontSize: 12, color: 'var(--accent)' }}
        >
          {comment.by}
        </span>
        <span style={{ color: 'var(--text-muted)' }}>·</span>
        <span className="comment-meta">
          {comment.time ? timeAgo(comment.time) : 'unknown'}
        </span>
        {replyCount > 0 && (
          <>
            <span style={{ color: 'var(--text-muted)' }}>·</span>
            <span 
              className="font-body"
              style={{ fontSize: 11, color: 'var(--text-muted)' }}
            >
              {replyCount} repl{replyCount === 1 ? 'y' : 'ies'}
            </span>
          </>
        )}
      </div>
      
      {/* Comment Text */}
      <div 
        className="comment-text pl-5"
        dangerouslySetInnerHTML={{ __html: comment.text || '' }}
      />
      
      {/* Replies */}
      {comment.children && comment.children.length > 0 && (
        <div className="mt-2">
          {comment.children.map(child => (
            <CommentNode
              key={child.id}
              comment={child}
              onToggleCollapse={onToggleCollapse}
              timeAgo={timeAgo}
              depth={depth + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function countAllReplies(comment: HNComment): number {
  if (!comment.children || comment.children.length === 0) return 0;
  return comment.children.reduce((sum, child) => {
    return sum + 1 + countAllReplies(child);
  }, 0);
}

export default function CommentTree({ comments, onToggleCollapse, timeAgo }: CommentTreeProps) {
  const [allCollapsed, setAllCollapsed] = useState(false);
  
  const handleCollapseAll = () => {
    const newState = !allCollapsed;
    setAllCollapsed(newState);
    comments.forEach(c => {
      if (newState && !c.collapsed) {
        onToggleCollapse(c.id);
      } else if (!newState && c.collapsed) {
        onToggleCollapse(c.id);
      }
      // Also toggle children
      toggleChildren(c, newState, onToggleCollapse);
    });
  };
  
  return (
    <div className="w-full">
      {/* Comments Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 
          className="font-display font-normal"
          style={{ fontSize: 20, color: 'var(--text-primary)' }}
        >
          Comments ({comments.reduce((sum, c) => sum + 1 + countAllReplies(c), 0)})
        </h3>
        <button
          onClick={handleCollapseAll}
          className="action-pill"
        >
          {allCollapsed ? 'Expand all' : 'Collapse all'}
        </button>
      </div>
      
      {/* Comments */}
      <div>
        {comments.map(comment => (
          <CommentNode
            key={comment.id}
            comment={comment}
            onToggleCollapse={onToggleCollapse}
            timeAgo={timeAgo}
          />
        ))}
      </div>
    </div>
  );
}

function toggleChildren(
  comment: HNComment, 
  collapse: boolean, 
  onToggle: (id: number) => void
) {
  comment.children?.forEach(child => {
    if (collapse && !child.collapsed) {
      onToggle(child.id);
    } else if (!collapse && child.collapsed) {
      onToggle(child.id);
    }
    toggleChildren(child, collapse, onToggle);
  });
}
