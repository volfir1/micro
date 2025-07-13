import { useState, useCallback } from 'react';

export const useVibrationInput = () => {
  const [vibrationEnabled, setVibrationEnabled] = useState(false);
  const [vibrationIntensity, setVibrationIntensity] = useState(50);

  const handleVibrationToggle = useCallback((enabled) => {
    setVibrationEnabled(enabled);
  }, []);

  const handleIntensityChange = useCallback((intensity) => {
    setVibrationIntensity(intensity);
  }, []);

  return {
    vibrationEnabled,
    vibrationIntensity,
    handleVibrationToggle,
    handleIntensityChange,
    setVibrationEnabled,
    setVibrationIntensity
  };
};
