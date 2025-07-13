// src/shared/hooks/output/useLEDControl.js
import { useState, useCallback, useRef } from 'react';

// Configuration
const USE_REAL_DATA = true;
const API_ENDPOINT = 'http://localhost:5000/api/led-control';

export function useLEDControl() {
  const [ledState, setLedState] = useState({
    isEnabled: false,
    currentColor: '#ffffff',
    brightness: 50,
    isConnected: false,
    lastCommand: 'Never'
  });

  const [isLoading, setIsLoading] = useState(false);
  
  // Debounce timers
  const colorTimer = useRef(null);
  const brightnessTimer = useRef(null);
  
  // Send command to LED strip (optimized)
  const sendLEDCommand = useCallback(async (command) => {
    if (!USE_REAL_DATA) {
      // DUMMY DATA: Instant response
      setLedState(prev => ({
        ...prev,
        lastCommand: new Date().toLocaleTimeString(),
        isConnected: true
      }));
      return { success: true };
    }

    // REAL DATA: Send to backend
    try {
      const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(command),
      });

      if (!response.ok) throw new Error('Failed to send command');
      
      const data = await response.json();
      setLedState(prev => ({
        ...prev,
        isConnected: true,
        lastCommand: new Date().toLocaleTimeString()
      }));
      
      return data;
    } catch (error) {
      console.error('Error sending LED command:', error);
      setLedState(prev => ({ ...prev, isConnected: false }));
      throw error;
    }
  }, []);

  // Toggle LED power (instant)
  const togglePower = useCallback(async (enabled) => {
    // Update UI immediately
    setLedState(prev => ({
      ...prev,
      isEnabled: enabled
    }));

    // Send command
    try {
      await sendLEDCommand({
        type: 'power',
        enabled: enabled
      });
    } catch (error) {
      // Revert on error
      setLedState(prev => ({
        ...prev,
        isEnabled: !enabled
      }));
      console.error('Error toggling LED power:', error);
    }
  }, [sendLEDCommand]);

  // Change LED color (debounced)
  const changeColor = useCallback((color) => {
    // Update UI immediately
    setLedState(prev => ({
      ...prev,
      currentColor: color
    }));

    // Clear previous timer
    if (colorTimer.current) {
      clearTimeout(colorTimer.current);
    }

    // Debounce API call
    colorTimer.current = setTimeout(async () => {
      try {
        await sendLEDCommand({
          type: 'color',
          color: color,
          brightness: ledState.brightness
        });
      } catch (error) {
        console.error('Error changing LED color:', error);
      }
    }, 300); // 300ms delay
  }, [sendLEDCommand, ledState.brightness]);

  // Change brightness (debounced)
  const changeBrightness = useCallback((brightness) => {
    // Update UI immediately
    setLedState(prev => ({
      ...prev,
      brightness: brightness
    }));

    // Clear previous timer
    if (brightnessTimer.current) {
      clearTimeout(brightnessTimer.current);
    }

    // Debounce API call
    brightnessTimer.current = setTimeout(async () => {
      try {
        await sendLEDCommand({
          type: 'brightness',
          brightness: brightness
        });
      } catch (error) {
        console.error('Error changing brightness:', error);
      }
    }, 200); // 200ms delay
  }, [sendLEDCommand]);

  // Color presets - basic colors only
  const colorPresets = [
    { name: 'White', color: '#ffffff' },
    { name: 'Red', color: '#ff0000' },
    { name: 'Green', color: '#00ff00' },
    { name: 'Blue', color: '#0000ff' },
    { name: 'Yellow', color: '#ffff00' },
    { name: 'Purple', color: '#9900ff' },
    { name: 'Orange', color: '#ff6600' },
    { name: 'Pink', color: '#ff0099' },
  ];

  // Set preset color (instant)
  const setPresetColor = useCallback((color) => {
    if (ledState.isEnabled) {
      // Clear any pending color changes
      if (colorTimer.current) {
        clearTimeout(colorTimer.current);
      }
      
      // Update immediately and send command
      setLedState(prev => ({
        ...prev,
        currentColor: color
      }));
      
      // Send immediately for presets (no debounce)
      sendLEDCommand({
        type: 'color',
        color: color,
        brightness: ledState.brightness
      }).catch(error => {
        console.error('Error setting preset color:', error);
      });
    }
  }, [ledState.isEnabled, ledState.brightness, sendLEDCommand]);

  // Return optimized interface
  return {
    // State
    isEnabled: ledState.isEnabled,
    currentColor: ledState.currentColor,
    brightness: ledState.brightness,
    isConnected: ledState.isConnected,
    isLoading,
    
    // Actions (optimized)
    togglePower,        // Instant
    changeColor,        // Debounced 300ms
    changeBrightness,   // Debounced 200ms  
    setPresetColor,     // Instant
    
    // Constants
    colorPresets
  };
}