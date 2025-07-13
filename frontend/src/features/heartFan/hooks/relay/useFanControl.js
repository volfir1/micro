// src/shared/hooks/output/useFanControl.js
import { useState } from 'react';

export function useFanControl() {
  const [isOn, setIsOn] = useState(false);
  const [speed, setSpeed] = useState(50);

  const turnFan = (on) => {
    console.log(`Fan turned ${on ? 'on' : 'off'}`);
    setIsOn(on);
  };

  return {
    isOn,
    speed,
    turnFan,
    setSpeed
  };
}