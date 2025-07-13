import { useState, useCallback } from 'react';

export const useFanInput = () => {
  const [fanEnabled, setFanEnabled] = useState(false);
  const [fanSpeed, setFanSpeed] = useState(75);

  const handleFanToggle = useCallback((enabled) => {
    setFanEnabled(enabled);
  }, []);

  const handleSpeedChange = useCallback((speed) => {
    setFanSpeed(speed);
  }, []);

  return {
    fanEnabled,
    fanSpeed,
    handleFanToggle,
    handleSpeedChange,
    setFanEnabled,
    setFanSpeed
  };
};