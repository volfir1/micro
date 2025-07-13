import { useState, useEffect } from "react";

export function useSleepMonitor() {
  const [sleepData, setSleepData] = useState({
    status: "Awake",
    level: 20,
    duration: "00:00"
  });

  useEffect(() => {
    const start = Date.now();

    const interval = setInterval(() => {
      const elapsed = Math.floor((Date.now() - start) / 60000); // in minutes
      const newDuration = `${String(Math.floor(elapsed / 60)).padStart(2, "0")}:${String(elapsed % 60).padStart(2, "0")}`;

      const isSleeping = Math.random() > 0.3; // 70% chance of being asleep
      const level = isSleeping ? Math.floor(Math.random() * 30 + 70) : Math.floor(Math.random() * 40);

      setSleepData({
        status: isSleeping ? "Sleeping" : "Awake",
        level,
        duration: newDuration
      });
    }, 5000); // update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return sleepData;
}
