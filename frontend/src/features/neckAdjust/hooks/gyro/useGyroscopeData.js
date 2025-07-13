// src/shared/hooks/input/useGyroscopeData.js
import { useState, useEffect } from 'react';
import { useSystemState } from '@/features/useSystemState';

// Configuration
const USE_REAL_DATA = true;
const API_ENDPOINT = 'http://localhost:5000/api/gyroscope-data';

export function useGyroscopeData() {
  const { isInBed } = useSystemState(); // Monitor position whenever person is in bed
  const [gyroData, setGyroData] = useState({
    pitch: 0,
    roll: 0,
    neckAngle: 0,
    position: 'Unknown', // Back, Left Side, Right Side, etc.
    postureSeverity: 'Good', // Good, Poor, Bad
    lastUpdated: 'Never',
    isConnected: false
  });

  useEffect(() => {
    // Don't monitor position if not in bed
    if (!isInBed) {
      setGyroData(prev => ({
        ...prev,
        isConnected: false,
        position: 'Not in bed'
      }));
      return;
    }

    let interval;
    
    if (USE_REAL_DATA) {
      // REAL DATA: Connect to Raspberry Pi for MPU6050 data
      const fetchGyroData = async () => {
        try {
          const response = await fetch(API_ENDPOINT);
          
          if (!response.ok) throw new Error('Failed to fetch gyroscope data');
          
          const data = await response.json();
          
          // Calculate neck angle and position from raw data if not provided
          const neckAngle = data.neckAngle || Math.abs(data.pitch);
          let position = data.position;
          let postureSeverity = data.postureSeverity;
          
          if (!position) {
            // Calculate position from roll if not provided
            if (data.roll > 30) position = 'Right Side';
            else if (data.roll < -30) position = 'Left Side';
            else position = 'Back';
          }
          
          if (!postureSeverity) {
            // Determine posture severity from neck angle
            if (neckAngle < 15) postureSeverity = 'Good';
            else if (neckAngle < 30) postureSeverity = 'Poor';
            else postureSeverity = 'Bad';
          }
          
          setGyroData({
            pitch: data.pitch,
            roll: data.roll,
            neckAngle,
            position,
            postureSeverity,
            lastUpdated: new Date().toLocaleTimeString(),
            isConnected: true
          });
        } catch (error) {
          console.error('Error fetching gyroscope data:', error);
          setGyroData(prev => ({
            ...prev,
            isConnected: false
          }));
        }
      };
      
      fetchGyroData(); // Initial fetch
      interval = setInterval(fetchGyroData, 500); // Match 500ms delay from Arduino
    } else {
      // DUMMY DATA: Simulate realistic MPU6050 readings
      interval = setInterval(() => {
        // Generate realistic pitch/roll values
        const pitch = (Math.random() * 60) - 30; // -30 to +30 degrees
        const roll = (Math.random() * 60) - 30;  // -30 to +30 degrees
        const neckAngle = Math.abs(pitch);
        
        // Determine sleep position based on roll angle
        let position = 'Back';
        if (roll > 30) position = 'Right Side';
        else if (roll < -30) position = 'Left Side';
        
        // Determine posture quality based on neck angle
        let postureSeverity = 'Good';
        if (neckAngle > 30) postureSeverity = 'Bad';
        else if (neckAngle > 15) postureSeverity = 'Poor';
        
        setGyroData({
          pitch: parseFloat(pitch.toFixed(1)),
          roll: parseFloat(roll.toFixed(1)),
          neckAngle: parseFloat(neckAngle.toFixed(1)),
          position,
          postureSeverity,
          lastUpdated: new Date().toLocaleTimeString(),
          isConnected: true
        });
      }, 500); // Match the 500ms delay in Arduino code
    }

    return () => clearInterval(interval);
  }, [isInBed]);

  return gyroData;
}