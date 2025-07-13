import { useBodyWeight } from './weightLCD/hooks/weight/useBodyWeight';
import { useSleepMonitor } from './snoreAlarm/hooks/mic/useSnoreMonitor';

export function useSystemState() {
  const { weight } = useBodyWeight();
  const { status: sleepStatus } = useSleepMonitor();

  const isInBed = weight > 30;
  const isSleeping = isInBed && sleepStatus === 'Sleeping';
  const isAwake = isInBed && sleepStatus === 'Awake';

  return {
    isInBed,
    isSleeping,
    isAwake,
  };
}