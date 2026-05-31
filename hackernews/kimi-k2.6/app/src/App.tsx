import { Routes, Route, useNavigate, useLocation } from 'react-router';
import { useEffect, useCallback } from 'react';
import { Toaster } from '@/components/ui/sonner';
import Navbar from '@/components/Navbar';
import BottomBar from '@/components/BottomBar';
import SearchOverlay from '@/components/SearchOverlay';
import SettingsPanel from '@/components/SettingsPanel';
import Home from '@/pages/Home';
import StoryDetail from '@/pages/StoryDetail';
import { useHNStore } from '@/hooks/useHNStore';
import './App.css';

export default function App() {
  const navigate = useNavigate();
  const location = useLocation();
  const store = useHNStore();
  
  const isStoryPage = location.pathname.startsWith('/story/');
  const showBottomBar = !isStoryPage && !store.searchOpen && !store.settingsOpen;

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
      
      if (e.key === '/') {
        e.preventDefault();
        store.setSearchOpen(true);
      } else if (e.key === 'Escape') {
        if (store.searchOpen) {
          store.setSearchOpen(false);
        } else if (store.settingsOpen) {
          store.setSettingsOpen(false);
        } else if (isStoryPage) {
          navigate('/');
        }
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [store.searchOpen, store.settingsOpen, isStoryPage, navigate]);

  const handleRefresh = useCallback(() => {
    store.setPage(0);
    store.fetchStories(store.storyType, 0);
  }, [store]);

  return (
    <div 
      className="min-h-screen"
      style={{ backgroundColor: 'var(--canvas)' }}
    >
      <Toaster 
        position="top-center"
        toastOptions={{
          style: {
            backgroundColor: 'var(--surface)',
            color: 'var(--text-primary)',
            border: '1px solid var(--border)',
            fontFamily: 'Inter, sans-serif',
          },
        }}
      />
      
      {/* Navigation */}
      <Navbar
        onSearchOpen={() => store.setSearchOpen(true)}
        onSettingsOpen={() => store.setSettingsOpen(true)}
        onRefresh={handleRefresh}
      />
      
      {/* Main Content */}
      <Routes>
        <Route 
          path="/" 
          element={
            <Home
              stories={store.stories}
              loading={store.loading}
              storyType={store.storyType}
              hideVisited={store.hideVisited}
              searchQuery={store.searchQuery}
              onFollow={store.toggleFollow}
              timeAgo={store.timeAgo}
              onFetchStories={store.fetchStories}
              onStoryTypeChange={store.setStoryType}
              page={store.page}
              setPage={store.setPage}
            />
          } 
        />
        <Route 
          path="/story/:id" 
          element={
            <StoryDetail
              currentStory={store.currentStory}
              comments={store.comments}
              loading={store.loading}
              timeAgo={store.timeAgo}
              onFetchStory={store.fetchStoryWithComments}
              onToggleFollow={store.toggleFollow}
              onToggleCommentCollapse={store.toggleCommentCollapse}
            />
          } 
        />
      </Routes>
      
      {/* Bottom Bar */}
      {showBottomBar && (
        <BottomBar
          storyType={store.storyType}
          onStoryTypeChange={store.setStoryType}
          hideVisited={store.hideVisited}
          onHideVisitedChange={store.setHideVisited}
          page={store.page}
        />
      )}
      
      {/* Search Overlay */}
      <SearchOverlay
        isOpen={store.searchOpen}
        onClose={() => store.setSearchOpen(false)}
        searchQuery={store.searchQuery}
        onSearchChange={store.setSearchQuery}
      />
      
      {/* Settings Panel */}
      <SettingsPanel
        isOpen={store.settingsOpen}
        onClose={() => store.setSettingsOpen(false)}
        darkMode={store.darkMode}
        onDarkModeChange={store.setDarkMode}
        onClearVisited={store.clearVisited}
        onClearFollowed={store.clearFollowed}
      />
    </div>
  );
}
