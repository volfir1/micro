import { useState, useCallback } from 'react';

export const useFanOutput = () => {
  const [fanStatus, setFanStatus] = useState('idle');
  const [fanError, setFanError] = useState(null);

  const controlFan = useCallback(async (enabled, speed) => {
    setFanStatus('updating');
    // API call will be made through service
  }, []);

  const getFanStatus = useCallback(() => {
    return { status: fanStatus, error: fanError };
  }, [fanStatus, fanError]);

  return {
    fanStatus,
    fanError,
    controlFan,
    getFanStatus,
    setFanStatus,
    setFanError
  };
};