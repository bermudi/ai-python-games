import { useEffect, useRef, useState, useCallback } from 'react';
import type { HNStory, StoryType } from '@/types/hn';
import StoryRow from './StoryRow';
import { Skeleton } from '@/components/ui/skeleton';

interface StoryListProps {
  stories: HNStory[];
  loading: boolean;
  storyType: StoryType;
  hideVisited: boolean;
  searchQuery: string;
  onFollow: (storyId: number) => void;
  timeAgo: (timestamp: number) => string;
  onLoadMore: () => void;
  hasMore: boolean;
}

export default function StoryList({
  stories,
  loading,
  storyType,
  hideVisited,
  searchQuery,
  onFollow,
  timeAgo,
  onLoadMore,
  hasMore,
}: StoryListProps) {
  const [visibleStories, setVisibleStories] = useState<Set<number>>(new Set());
  const observerRef = useRef<IntersectionObserver | null>(null);
  const listRef = useRef<HTMLDivElement>(null);
  
  const observeStory = useCallback((id: number, el: HTMLDivElement | null) => {
    if (!el) return;
    if (!observerRef.current) {
      observerRef.current = new IntersectionObserver(
        (entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              const storyId = Number((entry.target as HTMLElement).dataset.storyId);
              setVisibleStories(prev => new Set(prev).add(storyId));
            }
          });
        },
        { threshold: 0.1 }
      );
    }
    el.dataset.storyId = String(id);
    observerRef.current.observe(el);
  }, []);
  
  useEffect(() => {
    return () => {
      observerRef.current?.disconnect();
    };
  }, []);

  const typeLabels: Record<StoryType, string> = {
    top: 'Top Stories',
    new: 'New Stories',
    best: 'Best Stories',
  };

  const filteredStories = stories.filter(story => {
    if (hideVisited && story.visited) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      return (
        story.title?.toLowerCase().includes(q) ||
        story.by?.toLowerCase().includes(q) ||
        story.domain?.toLowerCase().includes(q)
      );
    }
    return true;
  });

  return (
    <div ref={listRef} className="w-full max-w-[680px] mx-auto px-6 pt-16 pb-32">
      {/* Section Header */}
      <div className="flex items-center gap-3 mb-6">
        <h2 
          className="font-display font-normal"
          style={{ 
            fontSize: 24, 
            color: 'var(--text-primary)',
          }}
        >
          {searchQuery ? `Search: "${searchQuery}"` : typeLabels[storyType]}
        </h2>
        {searchQuery && (
          <span 
            className="category-badge"
          >
            {filteredStories.length} results
          </span>
        )}
      </div>
      
      {/* Story Rows */}
      <div className="divide-y" style={{ borderColor: 'var(--border-light)' }}>
        {filteredStories.map((story, index) => (
          <div 
            key={story.id}
            ref={el => observeStory(story.id, el)}
          >
            <StoryRow
              story={story}
              index={index}
              onFollow={onFollow}
              timeAgo={timeAgo}
              isVisible={visibleStories.has(story.id) || index < 10}
            />
          </div>
        ))}
        
        {/* Skeleton Loading */}
        {loading && (
          <>
            {[...Array(5)].map((_, i) => (
              <div key={`skeleton-${i}`} className="flex items-start gap-4 px-6 py-5">
                <div className="flex-shrink-0 w-12 flex justify-center pt-0.5">
                  <Skeleton className="h-6 w-10 rounded-xl" />
                </div>
                <div className="flex-1 space-y-2">
                  <Skeleton className="h-4 w-3/4" />
                  <Skeleton className="h-3 w-24" />
                  <Skeleton className="h-3 w-48" />
                </div>
              </div>
            ))}
          </>
        )}
      </div>
      
      {/* Empty State */}
      {!loading && filteredStories.length === 0 && (
        <div className="py-20 text-center">
          <p 
            className="font-body"
            style={{ fontSize: 14, color: 'var(--text-muted)' }}
          >
            {hideVisited 
              ? 'No unvisited stories found. Try turning off "Hide Visited".' 
              : searchQuery 
                ? 'No stories match your search.' 
                : 'No stories found.'}
          </p>
        </div>
      )}
      
      {/* Load More */}
      {hasMore && !loading && filteredStories.length > 0 && (
        <div className="flex justify-center mt-8">
          <button
            onClick={onLoadMore}
            className="action-pill"
          >
            Load more
          </button>
        </div>
      )}
    </div>
  );
}
