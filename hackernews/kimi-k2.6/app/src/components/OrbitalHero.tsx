import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ChevronDown } from 'lucide-react';

interface OrbitalHeroProps {
  onScrollDown: () => void;
}

export default function OrbitalHero({ onScrollDown }: OrbitalHeroProps) {
  const orbitRef = useRef<SVGSVGElement>(null);
  
  useEffect(() => {
    if (!orbitRef.current) return;
    
    const textPaths = orbitRef.current.querySelectorAll('.orbit-text');
    
    const animations = gsap.to(textPaths, {
      attr: { startOffset: '-100%' },
      duration: 24,
      repeat: -1,
      ease: 'none',
    });
    
    return () => {
      animations.kill();
    };
  }, []);
  
  return (
    <div 
      className="relative flex items-center justify-center min-h-screen"
      style={{ backgroundColor: 'var(--canvas)' }}
    >
      {/* Orbital Text Ring */}
      <div 
        className="absolute"
        style={{ 
          width: 280, 
          height: 280, 
          opacity: 0.4,
        }}
      >
        <svg 
          ref={orbitRef}
          viewBox="0 0 280 280" 
          width="280" 
          height="280"
          style={{ overflow: 'visible' }}
        >
          <defs>
            <path 
              id="orbitPath" 
              d="M 140, 140 m -120, 0 a 120,120 0 1,1 240,0 a 120,120 0 1,1 -240,0" 
            />
          </defs>
          <text 
            style={{ 
              fontFamily: 'Inter, sans-serif', 
              fontSize: 11, 
              textTransform: 'uppercase', 
              letterSpacing: 2,
              fill: 'var(--text-muted)',
            }}
          >
            <textPath 
              href="#orbitPath" 
              startOffset="0%" 
              className="orbit-text"
            >
              A CALM WAY TO READ HACKER NEWS&nbsp;&middot;&nbsp;
            </textPath>
            <textPath 
              href="#orbitPath" 
              startOffset="0%" 
              className="orbit-text"
            >
              A CALM WAY TO READ HACKER NEWS&nbsp;&middot;&nbsp;
            </textPath>
          </text>
        </svg>
      </div>
      
      {/* Center Content */}
      <div className="relative z-10 text-center">
        <h1 
          className="font-display font-light tracking-tight"
          style={{ 
            fontSize: 48, 
            letterSpacing: '-0.5px', 
            color: 'var(--text-primary)',
          }}
        >
          HN Zen
        </h1>
        <p 
          className="mt-3 font-body font-normal"
          style={{ 
            fontSize: 14, 
            color: 'var(--text-secondary)',
          }}
        >
          A calm way to read Hacker News
        </p>
      </div>
      
      {/* Scroll Down Chevron */}
      <button
        onClick={onScrollDown}
        className="absolute bottom-12 left-1/2 -translate-x-1/2 p-2 transition-colors hover:opacity-70 animate-bounce"
        style={{ color: 'var(--text-muted)' }}
      >
        <ChevronDown size={16} />
      </button>
    </div>
  );
}
