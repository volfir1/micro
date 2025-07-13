// src/shared/hooks/input/useSnoreDetection.js
import { useState, useEffect } from 'react';
import { useSystemState } from '@/features/useSystemState';

// Configuration - Toggle between real and dummy data
const USE_REAL_DATA = true; // Set to true when ready for production
const API_ENDPOINT = 'http://localhost:5000/api/snore-data';

export function useSnoreDetection() {
  const { isSleeping } = useSystemState();
  const [snoreData, setSnoreData] = useState({
    duration: "0h 0m",
    lastDetected: "Never",
    frequency: "0 Episodes",
    isDetected: false,
    isConnected: false // Add connection status
  });

  useEffect(() => {
    // Don't run detection if not sleeping
    if (!isSleeping) {
      setSnoreData(prev => ({
        ...prev,
        isDetected: false
      }));
      return;
    }

    let interval;
    
    if (USE_REAL_DATA) {
      // REAL DATA: Connect to Raspberry Pi
      const fetchSnoreData = async () => {
        try {
          const response = await fetch(API_ENDPOINT);
          
          if (!response.ok) throw new Error('Failed to fetch snore data');
          
          const data = await response.json();
          setSnoreData({
            ...data,
            isConnected: true
          });
        } catch (error) {
          console.error('Error fetching snore data:', error);
          setSnoreData(prev => ({
            ...prev,
            isConnected: false
          }));
        }
      };
      
      fetchSnoreData(); // Initial fetch
      interval = setInterval(fetchSnoreData, 3000);
    } else {
      // DUMMY DATA: Same as your current implementation
      interval = setInterval(() => {
        // Your existing code for dummy data
        const snoreDetected = Math.random() > 0.7;
        
        if (snoreDetected) {
          // existing dummy data logic
        } else {
          // existing else branch
        }
      }, 3000);
    }

    return () => clearInterval(interval);
  }, [isSleeping]);

  return snoreData;
}