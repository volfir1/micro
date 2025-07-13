import { useState, useCallback, useRef } from 'react';

export const usePillowInput = () => {
  const [pillowHeight, setPillowHeight] = useState(50);
  const pillowTimer = useRef(null);

  const handlePillowAdjust = useCallback((height) => {
    setPillowHeight(height);
  }, []);

  const handlePillowPreset = useCallback((preset) => {
    const height = preset === 'lower' ? 0 : 100;
    setPillowHeight(height);
  }, []);

  return {
    pillowHeight,
    handlePillowAdjust,
    handlePillowPreset,
    setPillowHeight,
    pillowTimer
  };
};