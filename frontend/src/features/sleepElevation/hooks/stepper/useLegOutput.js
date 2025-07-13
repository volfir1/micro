import { useState, useCallback } from 'react';

export const useLegOutput = () => {
  const [legStatus, setLegStatus] = useState('idle');
  const [legError, setLegError] = useState(null);

  const adjustLegs = useCallback(async (height) => {
    setLegStatus('adjusting');
    // API call will be made through service
  }, []);

  const getLegStatus = useCallback(() => {
    return { status: legStatus, error: legError };
  }, [legStatus, legError]);

  return {
    legStatus,
    legError,
    adjustLegs,
    getLegStatus,
    setLegStatus,
    setLegError
  };
};
