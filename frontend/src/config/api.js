// Frontend configuration for API endpoints
// Update these values when deploying to production

export const API_CONFIG = {
  // Set to true when backend is ready
  USE_REAL_DATA: true,
  
  // Backend URL - Change this to your Raspberry Pi's IP when deploying
  BASE_URL: 'http://localhost:5000', // For localhost testing
  // For Raspberry Pi: 'http://192.168.1.100:5000'
  
  // API endpoints
  ENDPOINTS: {
    HEART_RATE: '/api/heart-rate',
    BREATHING: '/api/breathing-data',
    GYROSCOPE: '/api/gyroscope-data',
    WEIGHT: '/api/weight-data',
    SNORE: '/api/snore-data',
    SLEEP_HISTORY: '/api/sleep-history',
    
    // Device controls
    FAN_CONTROL: '/api/control/fan',
    PILLOW_CONTROL: '/api/control/pillow',
    SPEAKER_CONTROL: '/api/control/speaker',
  },
  
  // WebSocket URL for real-time updates
  WEBSOCKET_URL: 'ws://192.168.1.100:5000',
  
  // Update intervals (milliseconds)
  UPDATE_INTERVALS: {
    HEART_RATE: 2000,
    BREATHING: 2000,
    GYROSCOPE: 500,
    WEIGHT: 5000,
    SNORE: 3000,
  }
};

// Helper function to get full URL
export const getApiUrl = (endpoint) => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
};

// Helper function to check if real data should be used
export const useRealData = () => {
  return API_CONFIG.USE_REAL_DATA;
};
