import { useState, useCallback, useRef } from 'react';
import { Box, Card, Group, Title, Text, Switch, Button, Slider, ColorPicker, Stack, Grid, Select, FileInput, Tabs, TextInput } from '@mantine/core';
import { AppIcons } from '@/shared/components/icons/AppIcons';
import { useLEDControl } from '@/features/weightLCD/hooks/lcd/useLedLight';
import { API_CONFIG } from '@/config/api';

// Helper function for API calls
const makeApiCall = async (endpoint, data = {}) => {
  try {
    const response = await fetch(`${API_CONFIG.BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    console.log(`API Success:`, result);
    return result;
  } catch (error) {
    console.error(`API Error for ${endpoint}:`, error);
    return { status: 'error', message: error.message };
  }
};

export default function DeviceControls() {
  const { Snore, Fan, Pillow, Leg, Vibration, Light } = AppIcons;
  
  // Device states
  const [alarmEnabled, setAlarmEnabled] = useState(false);
  const [fanEnabled, setFanEnabled] = useState(false);
  const [vibrationEnabled, setVibrationEnabled] = useState(false);
  const [pillowHeight, setPillowHeight] = useState(50);
  const [legHeight, setLegHeight] = useState(50);
  
  // Enhanced Music/Speaker states
  const [selectedMusic, setSelectedMusic] = useState('gentle_waves.mp3');
  const [customMusicFile, setCustomMusicFile] = useState(null);
  const [customMusicUrl, setCustomMusicUrl] = useState('');
  const [musicSelectionType, setMusicSelectionType] = useState('preset'); // 'preset', 'upload', 'url'
  const [uploadedMusicList, setUploadedMusicList] = useState([]); // Store uploaded files
  
  const [availableMusic, setAvailableMusic] = useState([
    { value: 'gentle_waves.mp3', label: '🌊 Gentle Waves' },
    { value: 'birds_chirping.mp3', label: '🐦 Birds Chirping' },
    { value: 'soft_piano.mp3', label: '🎹 Soft Piano' },
    { value: 'nature_sounds.mp3', label: '🌲 Nature Sounds' },
    { value: 'white_noise.mp3', label: '⚪ White Noise' },
    { value: 'classical_morning.mp3', label: '🎼 Classical Morning' },
    { value: 'meditation_bells.mp3', label: '🔔 Meditation Bells' },
    { value: 'rain_sounds.mp3', label: '🌧️ Rain Sounds' }
  ]);
  
  const [volume, setVolume] = useState(50);
  const [isPlaying, setIsPlaying] = useState(false);
  
  // Debounce timers
  const pillowTimer = useRef(null);
  const legTimer = useRef(null);
  const volumeTimer = useRef(null);
  
  // LED control hook
  const {
    isEnabled: ledEnabled,
    currentColor,
    brightness,
    isConnected,
    isLoading,
    togglePower,
    changeColor,
    changeBrightness,
    setPresetColor,
    colorPresets
  } = useLEDControl();
  
  // Get current music source based on selection type
  const getCurrentMusicSource = () => {
    switch (musicSelectionType) {
      case 'preset':
        return selectedMusic;
      case 'upload':
        return customMusicFile ? customMusicFile.name : null;
      case 'url':
        return customMusicUrl;
      default:
        return selectedMusic;
    }
  };
  
  // Handle file upload
  const handleFileUpload = useCallback(async (file) => {
    if (!file) return;
    
    setCustomMusicFile(file);
    
    // Create FormData to upload the file
    const formData = new FormData();
    formData.append('music_file', file);
    
    try {
      // Upload file to server
      const response = await fetch(`${API_CONFIG.BASE_URL}/api/upload/music`, {
        method: 'POST',
        body: formData
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('File uploaded successfully:', result);
        
        // Add to uploaded music list
        const newMusic = {
          value: result.filename || file.name,
          label: `🎵 ${file.name}`,
          isCustom: true
        };
        
        setUploadedMusicList(prev => [...prev, newMusic]);
      }
    } catch (error) {
      console.error('Upload failed:', error);
    }
  }, []);
  
  // Enhanced alarm toggle with different music source types
  const handleAlarmToggle = useCallback(async (enabled) => {
    setAlarmEnabled(enabled);
    
    if (!enabled && isPlaying) {
      await makeApiCall('/api/control/speaker', {
        action: 'stop'
      });
      setIsPlaying(false);
    }
    
    const musicSource = getCurrentMusicSource();
    
    await makeApiCall('/api/control/speaker', {
      action: 'set_alarm_state',
      enabled: enabled,
      music_source: musicSource,
      music_type: musicSelectionType,
      volume: volume
    });
  }, [musicSelectionType, selectedMusic, customMusicFile, customMusicUrl, volume, isPlaying]);
  
  // Enhanced music test with different source types
  const handleMusicTest = useCallback(async () => {
    if (!alarmEnabled) return;
    
    const musicSource = getCurrentMusicSource();
    if (!musicSource) return;
    
    if (isPlaying) {
      await makeApiCall('/api/control/speaker', {
        action: 'stop'
      });
      setIsPlaying(false);
    } else {
      await makeApiCall('/api/control/speaker', {
        action: 'play',
        music_source: musicSource,
        music_type: musicSelectionType,
        volume: volume,
        duration: 10000
      });
      setIsPlaying(true);
      
      setTimeout(() => {
        setIsPlaying(false);
      }, 10000);
    }
  }, [alarmEnabled, musicSelectionType, selectedMusic, customMusicFile, customMusicUrl, volume, isPlaying]);
  
  const handleMusicChange = useCallback(async (musicFile) => {
    setSelectedMusic(musicFile);
    
    if (alarmEnabled) {
      await makeApiCall('/api/control/speaker', {
        action: 'set_music',
        music_source: musicFile,
        music_type: 'preset',
        volume: volume
      });
    }
  }, [alarmEnabled, volume]);
  
  const handleVolumeChange = useCallback((newVolume) => {
    setVolume(newVolume);
    
    if (volumeTimer.current) {
      clearTimeout(volumeTimer.current);
    }
    
    volumeTimer.current = setTimeout(async () => {
      await makeApiCall('/api/control/speaker', {
        action: 'set_volume',
        volume: newVolume
      });
    }, 300);
  }, []);
  
  // Other device functions (unchanged)
  const handleFanToggle = useCallback(async (enabled) => {
    setFanEnabled(enabled);
    await makeApiCall('/api/control/fan', {
      state: enabled,
      speed: 75
    });
  }, []);
  
  const handleVibrationToggle = useCallback(async (enabled) => {
    setVibrationEnabled(enabled);
    await makeApiCall('/api/control/vibration', {
      state: enabled,
      intensity: 50
    });
  }, []);
  
  const handlePillowAdjust = useCallback((height) => {
    setPillowHeight(height);
    
    if (pillowTimer.current) {
      clearTimeout(pillowTimer.current);
    }
    
    pillowTimer.current = setTimeout(async () => {
      const angle = (height - 50) * 0.9;
      await makeApiCall('/api/control/pillow', {
        height: height,
        angle: angle
      });
    }, 300);
  }, []);
  
  const handleLegAdjust = useCallback((height) => {
    setLegHeight(height);
    
    if (legTimer.current) {
      clearTimeout(legTimer.current);
    }
    
    legTimer.current = setTimeout(async () => {
      await makeApiCall('/api/control/legs', {
        height: height,
        angle: height * 0.6
      });
    }, 300);
  }, []);

  return (
    <Box p="xl">
      <Stack gap="xs" mb="xl">
        <Title order={2}>Device Controls</Title>
        <Text c="dimmed">Manage and test your hardware outputs.</Text>
      </Stack>
      
      <Grid gutter="xl">
        {/* Enhanced Speaker/Music System with Custom Music Support */}
        <Grid.Col span={{ base: 12, md: 12, lg: 6 }}>
          <Card withBorder radius="md" p="xl">
            <Stack gap="md">
              <Group justify="space-between">
                <Group gap="sm">
                  <Snore size={28} />
                  <Title order={4}>Speaker / Wake-up Music</Title>
                </Group>
                <Switch 
                  checked={alarmEnabled} 
                  onChange={(e) => handleAlarmToggle(e.currentTarget.checked)} 
                />
              </Group>
              
              {alarmEnabled && (
                <Stack gap="sm">
                  <Text fw={500} size="sm">Music Selection</Text>
                  
                  {/* Music Source Tabs */}
                  <Tabs value={musicSelectionType} onChange={setMusicSelectionType}>
                    <Tabs.List>
                      <Tabs.Tab value="preset">🎵 Presets</Tabs.Tab>
                      <Tabs.Tab value="upload">📁 Upload File</Tabs.Tab>
                      <Tabs.Tab value="url">🌐 URL/Stream</Tabs.Tab>
                    </Tabs.List>

                    <Tabs.Panel value="preset" pt="sm">
                      <Select
                        value={selectedMusic}
                        onChange={handleMusicChange}
                        data={[...availableMusic, ...uploadedMusicList]}
                        placeholder="Choose preset music"
                      />
                    </Tabs.Panel>

                    <Tabs.Panel value="upload" pt="sm">
                      <Stack gap="sm">
                        <FileInput
                          value={customMusicFile}
                          onChange={handleFileUpload}
                          placeholder="Choose music file"
                          accept="audio/*"
                          clearable
                        />
                        {customMusicFile && (
                          <Text size="sm" c="green">
                            ✓ Selected: {customMusicFile.name}
                          </Text>
                        )}
                      </Stack>
                    </Tabs.Panel>

                    <Tabs.Panel value="url" pt="sm">
                      <TextInput
                        value={customMusicUrl}
                        onChange={(e) => setCustomMusicUrl(e.currentTarget.value)}
                        placeholder="Enter music URL or streaming link"
                      />
                    </Tabs.Panel>
                  </Tabs>
                  
                  <Group grow>
                    <div>
                      <Text fw={500} size="sm">Volume: {volume}%</Text>
                      <Slider
                        value={volume}
                        onChange={handleVolumeChange}
                        min={1}
                        max={100}
                        step={1}
                      />
                    </div>
                  </Group>
                  
                  <Button 
                    onClick={handleMusicTest}
                    variant={isPlaying ? "filled" : "outline"}
                    color={isPlaying ? "red" : "blue"}
                    disabled={!getCurrentMusicSource()}
                  >
                    {isPlaying ? "⏹️ Stop Preview" : "▶️ Test Music (10s)"}
                  </Button>
                  
                  <Text size="xs" c="dimmed">
                    💡 Auto-plays when 3+ snores detected
                  </Text>
                </Stack>
              )}
            </Stack>
          </Card>
        </Grid.Col>

        {/* Fan */}
        <Grid.Col span={{ base: 12, md: 6, lg: 3 }}>
          <Card withBorder radius="md" p="xl">
            <Stack gap="md">
              <Group justify="space-between">
                <Group gap="sm">
                  <Fan size={28} />
                  <Title order={4}>Fan</Title>
                </Group>
                <Switch 
                  checked={fanEnabled} 
                  onChange={(e) => handleFanToggle(e.currentTarget.checked)} 
                />
              </Group>
            </Stack>
          </Card>
        </Grid.Col>

        {/* Bed Vibration */}
        <Grid.Col span={{ base: 12, md: 6, lg: 3 }}>
          <Card withBorder radius="md" p="xl">
            <Stack gap="md">
              <Group justify="space-between">
                <Group gap="sm">
                  <Vibration size={28} />
                  <Title order={4}>Bed Vibration</Title>
                </Group>
                <Switch 
                  checked={vibrationEnabled} 
                  onChange={(e) => handleVibrationToggle(e.currentTarget.checked)} 
                />
              </Group>
            </Stack>
          </Card>
        </Grid.Col>

        {/* Pillow Adjustment */}
        <Grid.Col span={{ base: 12, md: 6 }}>
          <Card withBorder radius="md" p="xl">
            <Stack gap="md">
              <Group gap="sm">
                <Pillow size={28} />
                <Title order={4}>Pillow Adjustment</Title>
              </Group>
              <Slider 
                value={pillowHeight} 
                onChange={handlePillowAdjust}
                min={0}
                max={100}
                step={1}
              />
              <Group justify="space-between">
                <Button onClick={() => handlePillowAdjust(0)}>Lower</Button>
                <Button onClick={() => handlePillowAdjust(100)}>Raise</Button>
              </Group>
            </Stack>
          </Card>
        </Grid.Col>

        {/* Leg Adjustment */}
        <Grid.Col span={{ base: 12, md: 6 }}>
          <Card withBorder radius="md" p="xl">
            <Stack gap="md">
              <Group gap="sm">
                <Leg size={28} />
                <Title order={4}>Leg Adjustment</Title>
              </Group>
              <Slider 
                value={legHeight} 
                onChange={handleLegAdjust}
                min={0}
                max={100}
                step={1}
              />
              <Group justify="space-between">
                <Button onClick={() => handleLegAdjust(0)}>Lower</Button>
                <Button onClick={() => handleLegAdjust(100)}>Raise</Button>
              </Group>
            </Stack>
          </Card>
        </Grid.Col>

        {/* LED Strip Lights */}
        <Grid.Col span={12}>
          <Card withBorder radius="md" p="xl">
            <Stack gap="md">
              <Group justify="space-between">
                <Group gap="sm">
                  <Light size={28} style={{ color: ledEnabled ? currentColor : '#868e96' }} />
                  <div>
                    <Title order={4}>LED Strip Lights</Title>
                    <Group gap="xs">
                      <div style={{ 
                        width: 8, 
                        height: 8, 
                        borderRadius: '50%', 
                        backgroundColor: isConnected ? '#51cf66' : '#ff6b6b' 
                      }} />
                      <Text size="xs" c="dimmed">
                        {isConnected ? 'Connected' : 'Disconnected'}
                      </Text>
                    </Group>
                  </div>
                </Group>
                <Switch 
                  checked={ledEnabled} 
                  onChange={(e) => togglePower(e.currentTarget.checked)}
                />
              </Group>

              {ledEnabled && (
                <Grid gutter="md">
                  <Grid.Col span={{ base: 12, md: 6 }}>
                    <Stack gap="sm">
                      <Text fw={500} size="sm">Color</Text>
                      <ColorPicker 
                        value={currentColor} 
                        onChange={changeColor}
                        fullWidth
                      />
                    </Stack>
                  </Grid.Col>

                  <Grid.Col span={{ base: 12, md: 6 }}>
                    <Stack gap="sm">
                      <Text fw={500} size="sm">Brightness: {brightness}%</Text>
                      <Slider
                        value={brightness}
                        onChange={changeBrightness}
                        min={1}
                        max={100}
                        step={1}
                      />
                    </Stack>
                  </Grid.Col>

                  <Grid.Col span={12}>
                    <Stack gap="xs">
                      <Text fw={500} size="sm">Quick Colors:</Text>
                      <Group gap="xs">
                        {colorPresets.map((preset) => (
                          <Button
                            key={preset.name}
                            size="xs"
                            variant="outline"
                            style={{ 
                              borderColor: preset.color,
                              color: preset.color
                            }}
                            onClick={() => setPresetColor(preset.color)}
                          >
                            {preset.name}
                          </Button>
                        ))}
                      </Group>
                    </Stack>
                  </Grid.Col>
                </Grid>
              )}
            </Stack>
          </Card>
        </Grid.Col>
      </Grid>
    </Box>
  );
}