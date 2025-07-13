import { useState, useEffect } from 'react';

export function useBodyWeight() {
  const [weightData, setWeightData] = useState({ weight: 0 });

  useEffect(() => {
    const interval = setInterval(() => {
      const isInBed = Math.random() > 0.4; // 60% chance someone is in bed
      const weight = isInBed ? Math.floor(Math.random() * 20) + 75 : 0;

      setWeightData({ weight });
    }, 7000); // Every 7 seconds

    return () => clearInterval(interval);
  }, []);

  return weightData;
}
