import { useState, useCallback, useRef } from 'react';

export const useLegInput = () => {
  const [legHeight, setLegHeight] = useState(50);
  const legTimer = useRef(null);

  const handleLegAdjust = useCallback((height) => {
    setLegHeight(height);
  }, []);

  const handleLegPreset = useCallback((preset) => {
    const height = preset === 'lower' ? 0 : 100;
    setLegHeight(height);
  }, []);

  return {
    legHeight,
    handleLegAdjust,
    handleLegPreset,
    setLegHeight,
    legTimer
  };
};