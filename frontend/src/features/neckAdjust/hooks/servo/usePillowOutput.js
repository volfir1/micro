import { useState, useCallback } from 'react';

export const usePillowOutput = () => {
  const [pillowStatus, setPillowStatus] = useState('idle');
  const [pillowError, setPillowError] = useState(null);

  const adjustPillow = useCallback(async (height) => {
    setPillowStatus('adjusting');
    // API call will be made through service
  }, []);

  const getPillowStatus = useCallback(() => {
    return { status: pillowStatus, error: pillowError };
  }, [pillowStatus, pillowError]);

  return {
    pillowStatus,
    pillowError,
    adjustPillow,
    getPillowStatus,
    setPillowStatus,
    setPillowError
  };
};