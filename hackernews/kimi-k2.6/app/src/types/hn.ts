export interface HNItem {
  id: number;
  title?: string;
  url?: string;
  text?: string;
  by?: string;
  time?: number;
  score?: number;
  descendants?: number;
  kids?: number[];
  type?: 'story' | 'comment' | 'job' | 'poll' | 'pollopt';
  deleted?: boolean;
  dead?: boolean;
  parent?: number;
}

export interface HNComment extends HNItem {
  type: 'comment';
  children?: HNComment[];
  collapsed?: boolean;
}

export interface HNStory extends HNItem {
  type: 'story';
  thumbnail?: string;
  domain?: string;
  visited?: boolean;
  following?: boolean;
  lastReadTime?: number;
  newCommentsCount?: number;
}

export type StoryType = 'top' | 'new' | 'best';

export interface AppState {
  stories: HNStory[];
  currentStory: HNStory | null;
  comments: HNComment[];
  loading: boolean;
  storyType: StoryType;
  page: number;
  hideVisited: boolean;
  searchQuery: string;
  settingsOpen: boolean;
  searchOpen: boolean;
  visitedStoryIds: Set<number>;
  followedStoryIds: Set<number>;
  followedStoriesLastRead: Record<number, number>;
  collapsedComments: Set<number>;
  darkMode: boolean;
}
