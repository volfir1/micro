import { useState, useCallback, useRef } from 'react';

export const useAudioInput = () => {
  const [selectedMusic, setSelectedMusic] = useState('gentle_waves.mp3');
  const [customMusicFile, setCustomMusicFile] = useState(null);
  const [customMusicUrl, setCustomMusicUrl] = useState('');
  const [musicSelectionType, setMusicSelectionType] = useState('preset');
  const [uploadedMusicList, setUploadedMusicList] = useState([]);
  const [volume, setVolume] = useState(50);
  
  const volumeTimer = useRef(null);
  
  const [availableMusic] = useState([
    { value: 'gentle_waves.mp3', label: '🌊 Gentle Waves' },
    { value: 'birds_chirping.mp3', label: '🐦 Birds Chirping' },
    { value: 'soft_piano.mp3', label: '🎹 Soft Piano' },
    { value: 'nature_sounds.mp3', label: '🌲 Nature Sounds' },
    { value: 'white_noise.mp3', label: '⚪ White Noise' },
    { value: 'classical_morning.mp3', label: '🎼 Classical Morning' },
    { value: 'meditation_bells.mp3', label: '🔔 Meditation Bells' },
    { value: 'rain_sounds.mp3', label: '🌧️ Rain Sounds' }
  ]);

  const getCurrentMusicSource = useCallback(() => {
    switch (musicSelectionType) {
      case 'preset': return selectedMusic;
      case 'upload': return customMusicFile ? customMusicFile.name : null;
      case 'url': return customMusicUrl;
      default: return selectedMusic;
    }
  }, [musicSelectionType, selectedMusic, customMusicFile, customMusicUrl]);

  const handleFileUpload = useCallback((file) => {
    if (!file) return;
    setCustomMusicFile(file);
  }, []);

  const handleMusicChange = useCallback((musicFile) => {
    setSelectedMusic(musicFile);
  }, []);

  const handleVolumeChange = useCallback((newVolume) => {
    setVolume(newVolume);
  }, []);

  const handleMusicTypeChange = useCallback((type) => {
    setMusicSelectionType(type);
  }, []);

  const handleUrlChange = useCallback((url) => {
    setCustomMusicUrl(url);
  }, []);

  return {
    selectedMusic, customMusicFile, customMusicUrl, musicSelectionType,
    uploadedMusicList, volume, availableMusic, getCurrentMusicSource,
    handleFileUpload, handleMusicChange, handleVolumeChange,
    handleMusicTypeChange, handleUrlChange, setUploadedMusicList
  };
};

// hooks/output/useAudioOutput.js
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

// hooks/input/usePillowInput.js
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