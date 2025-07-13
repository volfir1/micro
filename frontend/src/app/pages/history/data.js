export const sleepSessions = [
  {
    id: '1',
    date: 'Jun 23',
    duration: '6h 45m',
    sleepScore: 82,
    snoreEvents: 12,
    avgHR: 61,
    status: 'Good',
  },
  {
    id: '2',
    date: 'Jun 22',
    duration: '5h 10m',
    sleepScore: 60,
    snoreEvents: 24,
    avgHR: 72,
    status: 'Irregular',
  },
  {
    id: '3',
    date: 'Jun 21',
    duration: '7h 00m',
    sleepScore: 90,
    snoreEvents: 5,
    avgHR: 58,
    status: 'Good',
  },
  {
    id: '4',
    date: 'Jun 20',
    duration: '6h 30m',
    sleepScore: 75,
    snoreEvents: 18,
    avgHR: 65,
    status: 'Good',
  },
  {
    id: '5',
    date: 'Jun 19',
    duration: '4h 50m',
    sleepScore: 50,
    snoreEvents: 30,
    avgHR: 78,
    status: 'Irregular',
  },
];

export const sleepQualityData = [
  { date: 'Jun 19', score: 50, snoreCount: 30 },
  { date: 'Jun 20', score: 75, snoreCount: 18 },
  { date: 'Jun 21', score: 90, snoreCount: 5 },
  { date: 'Jun 22', score: 60, snoreCount: 24 },
  { date: 'Jun 23', score: 82, snoreCount: 12 },
];

export const heartRateAvgData = [
  { date: 'Jun 19', avgHR: 78 },
  { date: 'Jun 20', avgHR: 65 },
  { date: 'Jun 21', avgHR: 58 },
  { date: 'Jun 22', avgHR: 72 },
  { date: 'Jun 23', avgHR: 61 },
];

export const triggerLogs = [
  { timestamp: '2025-06-23 02:03 AM', action: 'Pillow Adjusted', reason: 'Bad Posture' },
  { timestamp: '2025-06-23 03:15 AM', action: 'Alarm Triggered', reason: 'Snore Detected' },
  { timestamp: '2025-06-22 01:45 AM', action: 'Fan Activated', reason: 'High Temperature' },
  { timestamp: '2025-06-22 04:00 AM', action: 'Pillow Adjusted', reason: 'Snore Detected' },
];
