import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router';
import { ArrowLeft, ExternalLink, Bell, BellOff, Share2 } from 'lucide-react';
import type { HNStory, HNComment } from '@/types/hn';
import CommentTree from '@/components/CommentTree';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from 'sonner';

interface StoryDetailProps {
  currentStory: HNStory | null;
  comments: HNComment[];
  loading: boolean;
  timeAgo: (timestamp: number) => string;
  onFetchStory: (storyId: number) => void;
  onToggleFollow: (storyId: number) => void;
  onToggleCommentCollapse: (commentId: number) => void;
}

export default function StoryDetail({
  currentStory,
  comments,
  loading,
  timeAgo,
  onFetchStory,
  onToggleFollow,
  onToggleCommentCollapse,
}: StoryDetailProps) {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [imageLoaded, setImageLoaded] = useState(false);
  
  useEffect(() => {
    if (id) {
      const storyId = parseInt(id, 10);
      onFetchStory(storyId);
    }
  }, [id]);
  
  const handleBack = () => {
    navigate('/');
  };
  
  const handleShare = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      toast.success('Link copied to clipboard');
    } catch {
      toast.error('Failed to copy link');
    }
  };

  if (loading && !currentStory) {
    return (
      <div 
        className="min-h-screen pt-16"
        style={{ backgroundColor: 'var(--canvas)' }}
      >
        <div className="max-w-[680px] mx-auto px-6 py-8 space-y-6">
          <Skeleton className="h-8 w-32" />
          <Skeleton className="h-12 w-full" />
          <Skeleton className="h-4 w-48" />
          <Skeleton className="h-64 w-full rounded-lg" />
          <Skeleton className="h-32 w-full" />
        </div>
      </div>
    );
  }
  
  if (!currentStory) {
    return (
      <div 
        className="min-h-screen pt-16 flex items-center justify-center"
        style={{ backgroundColor: 'var(--canvas)' }}
      >
        <p style={{ color: 'var(--text-muted)' }}>Story not found</p>
      </div>
    );
  }
  
  return (
    <div 
      className="min-h-screen pt-16"
      style={{ backgroundColor: 'var(--canvas)' }}
    >
      <div className="max-w-[680px] mx-auto px-6 py-8">
        {/* Back Button */}
        <button
          onClick={handleBack}
          className="flex items-center gap-2 mb-6 font-body transition-colors hover:opacity-70"
          style={{ fontSize: 13, color: 'var(--text-secondary)' }}
        >
          <ArrowLeft size={16} />
          All Stories
        </button>
        
        {/* Story Header */}
        <div className="mb-6">
          <h1 
            className="font-body font-semibold leading-snug"
            style={{ fontSize: 20, color: 'var(--text-primary)' }}
          >
            {currentStory.title}
          </h1>
          
          {/* Badges Row */}
          <div className="flex items-center gap-2 mt-3 flex-wrap">
            <span className="score-badge">
              {currentStory.score || 0} points
            </span>
            <span className="category-badge">
              {currentStory.domain}
            </span>
          </div>
          
          {/* Meta */}
          <div className="flex items-center gap-2 mt-2">
            <span 
              className="font-body"
              style={{ fontSize: 12, color: 'var(--text-secondary)' }}
            >
              by {currentStory.by}
            </span>
            <span style={{ color: 'var(--text-muted)' }}>·</span>
            <span 
              className="font-body"
              style={{ fontSize: 12, color: 'var(--text-secondary)' }}
            >
              {currentStory.time ? timeAgo(currentStory.time) : 'unknown'}
            </span>
          </div>
          
          {/* Actions */}
          <div className="flex items-center gap-2 mt-4 flex-wrap">
            {currentStory.url && (
              <a
                href={currentStory.url}
                target="_blank"
                rel="noopener noreferrer"
                className="action-pill flex items-center gap-1.5"
              >
                Read article
                <ExternalLink size={12} />
              </a>
            )}
            <button
              onClick={() => onToggleFollow(currentStory.id)}
              className="action-pill flex items-center gap-1.5"
              style={{
                backgroundColor: currentStory.following ? 'var(--accent)' : 'transparent',
                color: currentStory.following ? '#fff' : 'var(--text-secondary)',
                borderColor: currentStory.following ? 'var(--accent)' : 'var(--border)',
              }}
            >
              {currentStory.following ? <Bell size={12} /> : <BellOff size={12} />}
              {currentStory.following ? 'Following' : 'Follow thread'}
            </button>
            <button
              onClick={handleShare}
              className="action-pill flex items-center gap-1.5"
            >
              <Share2 size={12} />
              Share
            </button>
          </div>
        </div>
        
        {/* Thumbnail */}
        {currentStory.thumbnail && (
          <div 
            className="relative w-full overflow-hidden rounded-lg mb-8"
            style={{ 
              aspectRatio: '16/9',
              boxShadow: '0 2px 12px rgba(0,0,0,0.06)',
            }}
          >
            {!imageLoaded && (
              <Skeleton className="absolute inset-0 w-full h-full" />
            )}
            <img
              src={currentStory.thumbnail}
              alt={currentStory.title}
              className="w-full h-full object-cover transition-opacity duration-300"
              style={{ opacity: imageLoaded ? 1 : 0 }}
              onLoad={() => setImageLoaded(true)}
            />
          </div>
        )}
        
        {/* Story Text (if self-post) */}
        {currentStory.text && (
          <div 
            className="mb-8 font-serif leading-relaxed"
            style={{ 
              fontSize: 15, 
              lineHeight: 1.7, 
              color: 'var(--text-primary)',
            }}
            dangerouslySetInnerHTML={{ __html: currentStory.text }}
          />
        )}
        
        {/* Comments Section */}
        <div 
          className="pt-6"
          style={{ borderTop: '1px solid var(--border-light)' }}
        >
          {loading && comments.length === 0 ? (
            <div className="space-y-4">
              <Skeleton className="h-5 w-32" />
              <div className="space-y-3">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="space-y-2">
                    <Skeleton className="h-3 w-48" />
                    <Skeleton className="h-16 w-full" />
                  </div>
                ))}
              </div>
            </div>
          ) : comments.length > 0 ? (
            <CommentTree
              comments={comments}
              onToggleCollapse={onToggleCommentCollapse}
              timeAgo={timeAgo}
            />
          ) : (
            <p 
              className="text-center py-12 font-body"
              style={{ fontSize: 14, color: 'var(--text-muted)' }}
            >
              No comments yet.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
