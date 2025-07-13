// src/shared/hooks/input/useHeartRateData.js
import { useState, useEffect } from 'react';
import { useSystemState } from '@/features/useSystemState';

// Configuration
const USE_REAL_DATA = true;
const API_ENDPOINT = 'http://localhost:5000/api/heart-rate';

export function useHeartRateData() {
  const { isInBed } = useSystemState();
  const [heartRateData, setHeartRateData] = useState({
    rate: 0,
    status: "Not Monitored",
    min: 0,
    max: 0,
    average: 0,
    variability: 0,  // Heart rate variability (HRV) - important sleep metric
    lastUpdated: "Never",
    isConnected: false
  });

  useEffect(() => {
    // Don't monitor heart rate if not in bed
    if (!isInBed) {
      setHeartRateData(prev => ({
        ...prev,
        rate: 0,
        status: "Not Monitored",
        isConnected: false
      }));
      return;
    }

    let interval;
    let heartRateHistory = [];
    
    if (USE_REAL_DATA) {
      // REAL DATA: Connect to Raspberry Pi
      const fetchHeartRateData = async () => {
        try {
          const response = await fetch(API_ENDPOINT);
          
          if (!response.ok) throw new Error('Failed to fetch heart rate data');
          
          const data = await response.json();
          
          // Update history for variability and averages
          if (data.rate) {
            heartRateHistory.push(data.rate);
            // Keep history to last 10 readings
            if (heartRateHistory.length > 10) {
              heartRateHistory.shift();
            }
          }
          
          // Calculate derived metrics if not provided
          const min = data.min || Math.min(...heartRateHistory, data.rate);
          const max = data.max || Math.max(...heartRateHistory, data.rate);
          const average = data.average || 
            heartRateHistory.reduce((sum, rate) => sum + rate, 0) / heartRateHistory.length;
            
          // Calculate heart rate variability (difference between consecutive beats)
          let variability = data.variability;
          if (!variability && heartRateHistory.length > 1) {
            const differences = [];
            for (let i = 1; i < heartRateHistory.length; i++) {
              differences.push(Math.abs(heartRateHistory[i] - heartRateHistory[i-1]));
            }
            variability = differences.reduce((sum, diff) => sum + diff, 0) / differences.length;
          }
          
          // Determine status
          let status = data.status;
          if (!status) {
            const rate = data.rate;
            if (rate < 50) status = "Low";
            else if (rate > 100) status = "High";
            else status = "Normal";
          }
          
          setHeartRateData({
            rate: data.rate,
            status,
            min,
            max,
            average: Math.round(average),
            variability: variability ? Math.round(variability) : 0,
            lastUpdated: new Date().toLocaleTimeString(),
            isConnected: true
          });
        } catch (error) {
          console.error('Error fetching heart rate data:', error);
          setHeartRateData(prev => ({
            ...prev,
            isConnected: false
          }));
        }
      };
      
      fetchHeartRateData(); // Initial fetch
      interval = setInterval(fetchHeartRateData, 2000);
    } else {
      // DUMMY DATA: Enhanced simulation with realistic patterns
      interval = setInterval(() => {
        // Base rate with sleep-appropriate range (slower during sleep)
        const baseRate = 65; 
        const variance = Math.random() * 20 - 5; // -5 to +15
        const newRate = Math.floor(baseRate + variance);
        
        // Update history for variability calculation
        heartRateHistory.push(newRate);
        if (heartRateHistory.length > 10) {
          heartRateHistory.shift();
        }
        
        // Calculate heart rate variability (HRV)
        let variability = 0;
        if (heartRateHistory.length > 1) {
          const differences = [];
          for (let i = 1; i < heartRateHistory.length; i++) {
            differences.push(Math.abs(heartRateHistory[i] - heartRateHistory[i-1]));
          }
          variability = differences.reduce((sum, diff) => sum + diff, 0) / differences.length;
        }
        
        // Determine status
        let status = "Normal";
        if (newRate < 50) status = "Low";
        else if (newRate > 90) status = "High";
        
        // Calculate min, max, average
        const min = Math.min(...heartRateHistory);
        const max = Math.max(...heartRateHistory);
        const average = heartRateHistory.reduce((sum, rate) => sum + rate, 0) / heartRateHistory.length;
        
        setHeartRateData({
          rate: newRate,
          status,
          min,
          max,
          average: Math.round(average),
          variability: Math.round(variability),
          lastUpdated: new Date().toLocaleTimeString(),
          isConnected: true
        });
      }, 2000);
    }

    return () => clearInterval(interval);
  }, [isInBed]);

  return heartRateData;
}