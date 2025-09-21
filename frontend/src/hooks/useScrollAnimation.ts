"use client";

import { useEffect, useRef } from 'react';

interface ScrollAnimationOptions {
  translateY?: number;
  translateX?: number;
  opacity?: number;
  scale?: number;
  rotate?: number;
  duration?: number;
  delay?: number;
  easing?: string;
  threshold?: number;
}

export function useScrollAnimation(options: ScrollAnimationOptions = {}) {
  const elementRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const element = elementRef.current;
    if (!element) return;

    const {
      translateY = 50,
      translateX = 0,
      opacity = 0,
      scale = 0.8,
      rotate = 0,
      duration = 800,
      delay = 0,
      threshold = 0.1
    } = options;

    // Set initial state with CSS
    element.style.transform = `translateY(${translateY}px) translateX(${translateX}px) scale(${scale}) rotate(${rotate}deg)`;
    element.style.opacity = opacity.toString();
    element.style.transition = `transform ${duration}ms cubic-bezier(0.16, 1, 0.3, 1), opacity ${duration}ms cubic-bezier(0.16, 1, 0.3, 1)`;
    element.style.transitionDelay = `${delay}ms`;
    element.style.willChange = 'transform, opacity';
    element.style.backfaceVisibility = 'hidden';

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            // Animate to final state
            element.style.transform = 'translateY(0px) translateX(0px) scale(1) rotate(0deg)';
            element.style.opacity = '1';
          }
        });
      },
      { threshold }
    );

    observer.observe(element);

    return () => {
      observer.disconnect();
    };
  }, [options]);

  return elementRef;
}

export function useStaggeredAnimation(selector: string, options: ScrollAnimationOptions = {}) {
  const containerRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const {
      translateY = 30,
      translateX = 0,
      opacity = 0,
      scale = 0.8,
      duration = 600,
      delay = 100,
      threshold = 0.1
    } = options;

    const elements = container.querySelectorAll(selector) as NodeListOf<HTMLElement>;

    // Set initial state for all elements
    elements.forEach((element, index) => {
      element.style.transform = `translateY(${translateY}px) translateX(${translateX}px) scale(${scale})`;
      element.style.opacity = opacity.toString();
      element.style.transition = `all ${duration}ms cubic-bezier(0.16, 1, 0.3, 1)`;
      element.style.transitionDelay = `${index * delay}ms`;
    });

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            // Animate all elements to final state
            elements.forEach((element) => {
              element.style.transform = 'translateY(0px) translateX(0px) scale(1)';
              element.style.opacity = '1';
            });
          }
        });
      },
      { threshold }
    );

    observer.observe(container);

    return () => {
      observer.disconnect();
    };
  }, [selector, options]);

  return containerRef;
}