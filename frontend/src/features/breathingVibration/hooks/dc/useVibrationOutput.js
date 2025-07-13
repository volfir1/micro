import { useState, useCallback } from 'react';

export const useVibrationOutput = () => {
  const [vibrationStatus, setVibrationStatus] = useState('idle');
  const [vibrationError, setVibrationError] = useState(null);

  const controlVibration = useCallback(async (enabled, intensity) => {
    setVibrationStatus('updating');
    // API call will be made through service
  }, []);

  const getVibrationStatus = useCallback(() => {
    return { status: vibrationStatus, error: vibrationError };
  }, [vibrationStatus, vibrationError]);

  return {
    vibrationStatus,
    vibrationError,
    controlVibration,
    getVibrationStatus,
    setVibrationStatus,
    setVibrationError
  };
};