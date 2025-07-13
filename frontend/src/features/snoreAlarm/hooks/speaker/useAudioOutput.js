import { useState, useCallback } from 'react';

export const useAudioOutput = () => {
  const [alarmEnabled, setAlarmEnabled] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [deviceStatus, setDeviceStatus] = useState('idle');
  const [lastError, setLastError] = useState(null);

  const toggleAlarm = useCallback(async (enabled) => {
    setAlarmEnabled(enabled);
    setDeviceStatus('updating');
  }, []);

  const testMusic = useCallback(async () => {
    setIsPlaying(!isPlaying);
  }, [isPlaying]);

  const stopMusic = useCallback(async () => {
    setIsPlaying(false);
    setDeviceStatus('idle');
  }, []);

  return {
    alarmEnabled, isPlaying, deviceStatus, lastError,
    toggleAlarm, testMusic, stopMusic, setAlarmEnabled,
    setIsPlaying, setDeviceStatus, setLastError
  };
};