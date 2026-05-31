import { useState, useCallback, useEffect } from 'react';
import type { HNStory, HNComment, HNItem, StoryType } from '@/types/hn';

const STORIES_PER_PAGE = 30;

// Thumbnail mapping for fallback images
const THUMB_MAP: Record<string, string> = {
  'github.com': './images/thumb-code.jpg',
  'github.io': './images/thumb-code.jpg',
  'medium.com': './images/thumb-startup.jpg',
  'techcrunch.com': './images/thumb-startup.jpg',
  'theverge.com': './images/thumb-tech.jpg',
  'wired.com': './images/thumb-tech.jpg',
  'arstechnica.com': './images/thumb-tech.jpg',
  'huggingface.co': './images/thumb-ai.jpg',
  'openai.com': './images/thumb-ai.jpg',
  'anthropic.com': './images/thumb-ai.jpg',
  'ai': './images/thumb-ai.jpg',
  'machine learning': './images/thumb-ai.jpg',
  'llm': './images/thumb-ai.jpg',
  'startup': './images/thumb-startup.jpg',
  'funding': './images/thumb-startup.jpg',
  'acquired': './images/thumb-startup.jpg',
};

function getThumbnail(story: HNItem): string {
  // Try domain match
  if (story.url) {
    try {
      const domain = new URL(story.url).hostname.replace('www.', '');
      if (THUMB_MAP[domain]) return THUMB_MAP[domain];
      
      // Try partial domain match
      for (const [key, thumb] of Object.entries(THUMB_MAP)) {
        if (domain.includes(key) && key.length > 3) return thumb;
      }
    } catch {
      // ignore invalid URL
    }
  }
  
  // Try keyword match in title
  const title = (story.title || '').toLowerCase();
  for (const [key, thumb] of Object.entries(THUMB_MAP)) {
    if (title.includes(key)) return thumb;
  }
  
  // Default
  return './images/thumb-tech.jpg';
}

function extractDomain(url?: string): string {
  if (!url) return 'news.ycombinator.com';
  try {
    return new URL(url).hostname.replace('www.', '').toUpperCase();
  } catch {
    return 'news.ycombinator.com';
  }
}

function timeAgo(timestamp: number): string {
  const seconds = Math.floor((Date.now() / 1000) - timestamp);
  if (seconds < 60) return 'just now';
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
  const days = Math.floor(hours / 24);
  return `${days} day${days > 1 ? 's' : ''} ago`;
}

// localStorage helpers
function loadSet(key: string): Set<number> {
  try {
    const data = localStorage.getItem(key);
    return data ? new Set(JSON.parse(data)) : new Set();
  } catch {
    return new Set();
  }
}

function saveSet(key: string, set: Set<number>) {
  localStorage.setItem(key, JSON.stringify([...set]));
}

function loadRecord(key: string): Record<number, number> {
  try {
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : {};
  } catch {
    return {};
  }
}

function saveRecord(key: string, record: Record<number, number>) {
  localStorage.setItem(key, JSON.stringify(record));
}

export function useHNStore() {
  const [stories, setStories] = useState<HNStory[]>([]);
  const [currentStory, setCurrentStory] = useState<HNStory | null>(null);
  const [comments, setComments] = useState<HNComment[]>([]);
  const [loading, setLoading] = useState(false);
  const [storyType, setStoryType] = useState<StoryType>('top');
  const [page, setPage] = useState(0);
  const [hideVisited, setHideVisited] = useState(() => {
    return localStorage.getItem('hn_hide_visited') === 'true';
  });
  const [searchQuery, setSearchQuery] = useState('');
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [visitedStoryIds, setVisitedStoryIds] = useState<Set<number>>(() => loadSet('hn_visited'));
  const [followedStoryIds, setFollowedStoryIds] = useState<Set<number>>(() => loadSet('hn_followed'));
  const [followedStoriesLastRead, setFollowedStoriesLastRead] = useState<Record<number, number>>(() => loadRecord('hn_lastread'));
  const [collapsedComments, setCollapsedComments] = useState<Set<number>>(new Set());
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('hn_dark_mode');
    if (saved !== null) return saved === 'true';
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  // Apply dark mode
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('hn_dark_mode', String(darkMode));
  }, [darkMode]);

  // Persist visited
  useEffect(() => {
    saveSet('hn_visited', visitedStoryIds);
  }, [visitedStoryIds]);

  // Persist followed
  useEffect(() => {
    saveSet('hn_followed', followedStoryIds);
  }, [followedStoryIds]);

  // Persist last read
  useEffect(() => {
    saveRecord('hn_lastread', followedStoriesLastRead);
  }, [followedStoriesLastRead]);

  // Persist hide visited
  useEffect(() => {
    localStorage.setItem('hn_hide_visited', String(hideVisited));
  }, [hideVisited]);

  const fetchStories = useCallback(async (type: StoryType, pageNum: number) => {
    setLoading(true);
    try {
      const response = await fetch(`https://hacker-news.firebaseio.com/v0/${type}stories.json`);
      const storyIds: number[] = await response.json();
      
      const start = pageNum * STORIES_PER_PAGE;
      const end = start + STORIES_PER_PAGE;
      const pageIds = storyIds.slice(start, end);
      
      const storyPromises = pageIds.map(async (id) => {
        const res = await fetch(`https://hacker-news.firebaseio.com/v0/item/${id}.json`);
        const item: HNItem = await res.json();
        if (!item || item.deleted || item.dead) return null;
        return {
          ...item,
          type: 'story' as const,
          thumbnail: getThumbnail(item),
          domain: extractDomain(item.url),
          visited: visitedStoryIds.has(item.id),
          following: followedStoryIds.has(item.id),
        };
      });
      
      const results = (await Promise.all(storyPromises)).filter(Boolean) as HNStory[];
      
      if (pageNum === 0) {
        setStories(results);
      } else {
        setStories(prev => [...prev, ...results]);
      }
    } catch (error) {
      console.error('Failed to fetch stories:', error);
    } finally {
      setLoading(false);
    }
  }, [visitedStoryIds, followedStoryIds]);

  const fetchStoryWithComments = useCallback(async (storyId: number) => {
    setLoading(true);
    try {
      const res = await fetch(`https://hacker-news.firebaseio.com/v0/item/${storyId}.json`);
      const item: HNItem = await res.json();
      
      if (!item) return;
      
      const story: HNStory = {
        ...item,
        type: 'story',
        thumbnail: getThumbnail(item),
        domain: extractDomain(item.url),
        visited: true,
        following: followedStoryIds.has(item.id),
      };
      
      setCurrentStory(story);
      
      // Mark as visited
      setVisitedStoryIds(prev => {
        const next = new Set(prev);
        next.add(storyId);
        return next;
      });
      
      // Update last read time for followed stories
      if (followedStoryIds.has(storyId)) {
        setFollowedStoriesLastRead(prev => ({
          ...prev,
          [storyId]: Date.now(),
        }));
      }
      
      // Fetch comments recursively
      if (item.kids && item.kids.length > 0) {
        const commentTree = await fetchCommentsRecursively(item.kids);
        setComments(commentTree);
      } else {
        setComments([]);
      }
    } catch (error) {
      console.error('Failed to fetch story:', error);
    } finally {
      setLoading(false);
    }
  }, [followedStoryIds]);

  const fetchCommentsRecursively = async (kids: number[]): Promise<HNComment[]> => {
    const comments = await Promise.all(
      kids.map(async (kidId) => {
        try {
          const res = await fetch(`https://hacker-news.firebaseio.com/v0/item/${kidId}.json`);
          const item: HNItem = await res.json();
          if (!item || item.deleted || item.dead || item.type !== 'comment') return null;
          
          const comment: HNComment = {
            ...item,
            type: 'comment',
            children: item.kids && item.kids.length > 0 
              ? await fetchCommentsRecursively(item.kids) 
              : [],
            collapsed: collapsedComments.has(item.id),
          };
          
          return comment;
        } catch {
          return null;
        }
      })
    );
    
    return comments.filter(Boolean) as HNComment[];
  };

  const toggleFollow = useCallback((storyId: number) => {
    setFollowedStoryIds(prev => {
      const next = new Set(prev);
      if (next.has(storyId)) {
        next.delete(storyId);
        setFollowedStoriesLastRead(readPrev => {
          const readNext = { ...readPrev };
          delete readNext[storyId];
          return readNext;
        });
      } else {
        next.add(storyId);
        setFollowedStoriesLastRead(readPrev => ({
          ...readPrev,
          [storyId]: Date.now(),
        }));
      }
      return next;
    });
    
    setCurrentStory(prev => {
      if (!prev || prev.id !== storyId) return prev;
      return { ...prev, following: !prev.following };
    });
    
    setStories(prev => prev.map(s => 
      s.id === storyId ? { ...s, following: !s.following } : s
    ));
  }, []);

  const toggleCommentCollapse = useCallback((commentId: number) => {
    setCollapsedComments(prev => {
      const next = new Set(prev);
      if (next.has(commentId)) {
        next.delete(commentId);
      } else {
        next.add(commentId);
      }
      return next;
    });
    
    setComments(prev => updateCommentCollapse(prev, commentId));
  }, []);

  const clearVisited = useCallback(() => {
    setVisitedStoryIds(new Set());
    setStories(prev => prev.map(s => ({ ...s, visited: false })));
  }, []);

  const clearFollowed = useCallback(() => {
    setFollowedStoryIds(new Set());
    setFollowedStoriesLastRead({});
    setStories(prev => prev.map(s => ({ ...s, following: false })));
  }, []);

  return {
    stories,
    currentStory,
    comments,
    loading,
    storyType,
    page,
    hideVisited,
    searchQuery,
    settingsOpen,
    searchOpen,
    visitedStoryIds,
    followedStoryIds,
    followedStoriesLastRead,
    collapsedComments,
    darkMode,
    timeAgo,
    setStories,
    setCurrentStory,
    setComments,
    setLoading,
    setStoryType,
    setPage,
    setHideVisited,
    setSearchQuery,
    setSettingsOpen,
    setSearchOpen,
    setVisitedStoryIds,
    setDarkMode,
    fetchStories,
    fetchStoryWithComments,
    toggleFollow,
    toggleCommentCollapse,
    clearVisited,
    clearFollowed,
  };
}

function updateCommentCollapse(comments: HNComment[], targetId: number): HNComment[] {
  return comments.map(c => {
    if (c.id === targetId) {
      return { ...c, collapsed: !c.collapsed };
    }
    if (c.children && c.children.length > 0) {
      return { ...c, children: updateCommentCollapse(c.children, targetId) };
    }
    return c;
  });
}
