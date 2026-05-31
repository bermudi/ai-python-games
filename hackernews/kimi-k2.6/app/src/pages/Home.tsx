import { useEffect, useRef, useCallback } from 'react';
import OrbitalHero from '@/components/OrbitalHero';
import StoryList from '@/components/StoryList';
import type { HNStory, StoryType } from '@/types/hn';

interface HomeProps {
  stories: HNStory[];
  loading: boolean;
  storyType: StoryType;
  hideVisited: boolean;
  searchQuery: string;
  onFollow: (storyId: number) => void;
  timeAgo: (timestamp: number) => string;
  onFetchStories: (type: StoryType, page: number) => void;
  onStoryTypeChange: (type: StoryType) => void;
  page: number;
  setPage: (page: number) => void;
}

export default function Home({
  stories,
  loading,
  storyType,
  hideVisited,
  searchQuery,
  onFollow,
  timeAgo,
  onFetchStories,
  page,
  setPage,
}: HomeProps) {
  const heroRef = useRef<HTMLDivElement>(null);
  const hasFetched = useRef(false);

  // Initial fetch
  useEffect(() => {
    if (!hasFetched.current) {
      hasFetched.current = true;
      onFetchStories(storyType, 0);
    }
  }, []);

  // Fetch when story type changes
  useEffect(() => {
    if (hasFetched.current) {
      setPage(0);
      onFetchStories(storyType, 0);
    }
  }, [storyType]);

  const handleScrollDown = useCallback(() => {
    heroRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }, []);

  const handleLoadMore = useCallback(() => {
    const nextPage = page + 1;
    setPage(nextPage);
    onFetchStories(storyType, nextPage);
  }, [page, storyType, setPage, onFetchStories]);

  // Keyboard navigation
  useEffect(() => {
    let selectedIndex = -1;
    
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
      
      if (e.key === 'j' || e.key === 'J') {
        e.preventDefault();
        const visibleStories = document.querySelectorAll('.story-row');
        if (visibleStories.length === 0) return;
        selectedIndex = Math.min(selectedIndex + 1, visibleStories.length - 1);
        visibleStories[selectedIndex]?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      } else if (e.key === 'k' || e.key === 'K') {
        e.preventDefault();
        const visibleStories = document.querySelectorAll('.story-row');
        if (visibleStories.length === 0) return;
        selectedIndex = Math.max(selectedIndex - 1, 0);
        visibleStories[selectedIndex]?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [stories]);

  return (
    <div style={{ backgroundColor: 'var(--canvas)' }}>
      {/* Hero Section */}
      <div ref={heroRef}>
        <OrbitalHero onScrollDown={handleScrollDown} />
      </div>
      
      {/* Story List */}
      <StoryList
        stories={stories}
        loading={loading}
        storyType={storyType}
        hideVisited={hideVisited}
        searchQuery={searchQuery}
        onFollow={onFollow}
        timeAgo={timeAgo}
        onLoadMore={handleLoadMore}
        hasMore={true}
      />
    </div>
  );
}
