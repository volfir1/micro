// src/shared/hooks/input/useBreathingDetection.js
import { useState, useEffect } from 'react';
import { useSystemState } from '@/shared/hooks/useSystemState';

// Configuration
const USE_REAL_DATA = true;
const API_ENDPOINT = 'http://localhost:5000/api/breathing-data';

export function useBreathingDetection() {
  const { isInBed } = useSystemState(); // Note: we use isInBed instead of isSleeping since breathing should be monitored even when awake
  const [breathingData, setBreathingData] = useState({
    rate: 0,          // Breaths per minute
    rhythm: 'Normal', // Normal, Irregular, Shallow, Deep
    apneaEvents: 0,   // Count of breathing pauses
    lastMeasured: 'Never',
    isConnected: false
  });

  useEffect(() => {
    // Don't monitor breathing if not in bed
    if (!isInBed) {
      setBreathingData(prev => ({
        ...prev,
        rate: 0,
        rhythm: 'Not Monitored',
      }));
      return;
    }

    let interval;
    
    if (USE_REAL_DATA) {
      // REAL DATA: Connect to Raspberry Pi
      const fetchBreathingData = async () => {
        try {
          const response = await fetch(API_ENDPOINT);
          
          if (!response.ok) throw new Error('Failed to fetch breathing data');
          
          const data = await response.json();
          setBreathingData({
            ...data,
            isConnected: true,
            lastMeasured: new Date().toLocaleTimeString()
          });
        } catch (error) {
          console.error('Error fetching breathing data:', error);
          setBreathingData(prev => ({
            ...prev,
            isConnected: false
          }));
        }
      };
      
      fetchBreathingData(); // Initial fetch
      interval = setInterval(fetchBreathingData, 2000);
    } else {
      // DUMMY DATA: Generate realistic breathing patterns
      interval = setInterval(() => {
        // Generate realistic breathing rate (12-20 breaths per minute normally)
        // Vary it slightly each time for realism
        const baseRate = 14;
        const variance = Math.random() * 8 - 4; // -4 to +4
        const rate = Math.round(baseRate + variance);
        
        // Determine rhythm based on rate and randomness
        let rhythm = 'Normal';
        const rhythmRandom = Math.random();
        if (rate < 10) rhythm = 'Shallow';
        else if (rate > 20) rhythm = 'Deep';
        else if (rhythmRandom > 0.9) rhythm = 'Irregular'; // Occasional irregularity
        
        // Random chance for apnea event
        const newApneaEvent = Math.random() > 0.95;
        const apneaEvents = newApneaEvent ? 
          breathingData.apneaEvents + 1 : 
          breathingData.apneaEvents;
        
        setBreathingData({
          rate,
          rhythm,
          apneaEvents,
          lastMeasured: new Date().toLocaleTimeString(),
          isConnected: true
        });
      }, 2000);
    }

    return () => clearInterval(interval);
  }, [isInBed, breathingData.apneaEvents]);

  return breathingData;
}