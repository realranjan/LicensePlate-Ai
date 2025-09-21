"use client";

import React from 'react';
import { useScrollAnimation } from '@/hooks/useScrollAnimation';

interface ScrollRevealProps {
  children: React.ReactNode;
  direction?: 'up' | 'down' | 'left' | 'right';
  distance?: number;
  duration?: number;
  delay?: number;
  scale?: number;
  rotate?: number;
  className?: string;
  threshold?: number;
}

export function ScrollReveal({
  children,
  direction = 'up',
  distance = 50,
  duration = 800,
  delay = 0,
  scale = 1,
  rotate = 0,
  className = '',
  threshold = 0.1
}: ScrollRevealProps) {
  const getTranslateValues = () => {
    switch (direction) {
      case 'up':
        return { translateY: distance, translateX: 0 };
      case 'down':
        return { translateY: -distance, translateX: 0 };
      case 'left':
        return { translateY: 0, translateX: distance };
      case 'right':
        return { translateY: 0, translateX: -distance };
      default:
        return { translateY: distance, translateX: 0 };
    }
  };

  const { translateY, translateX } = getTranslateValues();

  const ref = useScrollAnimation({
    translateY,
    translateX,
    opacity: 0,
    scale,
    rotate,
    duration,
    delay,
    threshold
  });

  return (
    <div ref={ref} className={`${className} will-change-transform`} style={{ isolation: 'isolate' }}>
      {children}
    </div>
  );
}

export function StaggeredReveal({
  children,
  className = '',
  staggerDelay = 100,
  duration = 600,
  direction = 'up',
  distance = 30
}: {
  children: React.ReactNode;
  className?: string;
  staggerDelay?: number;
  duration?: number;
  direction?: 'up' | 'down' | 'left' | 'right';
  distance?: number;
}) {
  return (
    <div className={className}>
      {React.Children.map(children, (child, index) => (
        <ScrollReveal
          direction={direction}
          distance={distance}
          duration={duration}
          delay={index * staggerDelay}
        >
          {child}
        </ScrollReveal>
      ))}
    </div>
  );
}