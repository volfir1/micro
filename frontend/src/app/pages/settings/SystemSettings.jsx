import React from 'react';
import { Slider, Switch, Button, TextInput, ColorInput, Select, Group, Title, Paper, Text, Stack } from '@mantine/core';
import { AppIcons } from '../../../shared/components/icons/AppIcons';

export default function SystemSettings (){
  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <Title order={1} className="mb-8 text-gray-800">System Settings</Title>

      <Paper withBorder shadow="sm" p="lg" mb="xl" className="bg-white">
        <Title order={3} className="mb-4 text-gray-700 border-b pb-2">Sensor Thresholds</Title>
        <Stack>
          <div>
            <Text>Snore Sensitivity</Text>
            <Slider defaultValue={50} mt="xs" />
          </div>
          <div>
            <Text>Heart Rate Limits</Text>
            <Slider range defaultValue={[60, 100]} mt="xs" />
          </div>
          <div>
            <Text>Posture Angle Alert Level</Text>
            <Slider defaultValue={30} mt="xs" />
          </div>
        </Stack>
      </Paper>

      <Paper withBorder shadow="sm" p="lg" mb="xl" className="bg-white">
        <Title order={3} className="mb-4 text-gray-700 border-b pb-2">Alarm Settings</Title>
        <Stack>
          <Group position="apart">
            <Text>Alarm Volume</Text>
            <Slider className="w-1/2" />
          </Group>
          <Group position="apart">
            <Text>Alarm Duration (seconds)</Text>
            <TextInput type="number" defaultValue={10} className="w-1/2" />
          </Group>
          <Group position="apart">
            <Text>Repeat Cycle</Text>
            <Select
              className="w-1/2"
              data={[
                { value: 'once', label: 'Once' },
                { value: 'twice', label: 'Twice' },
                { value: 'continuous', label: 'Continuous' },
              ]}
            />
          </Group>
        </Stack>
      </Paper>

      <Paper withBorder shadow="sm" p="lg" mb="xl" className="bg-white">
        <Title order={3} className="mb-4 text-gray-700 border-b pb-2">Theme Preferences</Title>
        <Stack>
          <Group position="apart">
            <Text>Theme</Text>
            <Switch
              size="lg"
              onLabel={<AppIcons.Sun size={20} color="yellow" />}
              offLabel={<AppIcons.Moon size={20} color="blue" />}
            />
          </Group>
          <Group position="apart">
            <Text>Accent Color</Text>
            <ColorInput format="hex" defaultValue="#228be6" />
          </Group>
        </Stack>
      </Paper>

      <Paper withBorder shadow="sm" p="lg" mb="xl" className="bg-white">
        <Title order={3} className="mb-4 text-gray-700 border-b pb-2">Sleep Session Config</Title>
        <Stack>
            <Group position="apart">
                <Text>Auto-start Time</Text>
                <TextInput type="time" />
            </Group>
            <Group position="apart">
                <Text>Expected Duration (hours)</Text>
                <TextInput type="number" defaultValue={8} />
            </Group>
        </Stack>
      </Paper>

      <Paper withBorder shadow="sm" p="lg" mb="xl" className="bg-white">
        <Title order={3} className="mb-4 text-gray-700 border-b pb-2">System Access</Title>
        <Stack>
            <TextInput label="PIN" type="password" className="w-1/2" />
            <Button variant="outline" color="red" className="w-max">Reset PIN</Button>
        </Stack>
      </Paper>

      <Paper withBorder shadow="sm" p="lg" className="bg-white">
        <Title order={3} className="mb-4 text-gray-700 border-b pb-2">Optional Features</Title>
        <Stack>
            <Group position="apart">
                <Text>Developer Mode</Text>
                <Switch label="Show raw sensor logs" />
            </Group>
        </Stack>
      </Paper>

      <Group position="right" mt="xl">
        <Button variant="outline" color="gray" leftIcon={<AppIcons.Reset size={14} />}>
          Reset to Defaults
        </Button>
        <Button leftIcon={<AppIcons.Save size={14} />}>
          Save Settings
        </Button>
      </Group>
    </div>
  );
};

