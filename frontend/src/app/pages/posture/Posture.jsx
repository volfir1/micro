import { useState } from 'react';
import { Box, Card, Group, Title, Text, Badge, Stack, Grid, RingProgress, ThemeIcon, Center } from '@mantine/core';
import { AppIcons } from '@/shared/components/icons/AppIcons';
import { PostureMonitor } from '@/features/features';

export default function Posture() {
  const { Position, Foot } = AppIcons;

  // Mock data - in a real application, this would come from sensors/backend
 
  const [footElevation] = useState(10);
  const [lastChange] = useState('Rolled from back to side at 2:03 AM');
  const [autoResponse] = useState('Pillow Adjusted Due to Bad Posture');



  return (
    <Box p="xl">
      <Stack gap="xs" mb="xl">
        <Title order={2}>Posture & Position</Title>
        <Text c="dimmed">Real-time analysis of your sleep posture.</Text>
      </Stack>

      <Grid gutter="xl">
        <Grid.Col span={{ base: 12, lg: 6 }}>
          <Card withBorder radius="md" p="xl" h="100%">
            <Center style={{ height: '100%' }}>
              <Text c="dimmed">Camera Feed (Not available)</Text>
            </Center>
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, lg: 6 }}>
          <Stack gap="xl">
           <PostureMonitor />
            <Card withBorder radius="md" p="xl">
              <Group justify="space-between">
                <Group gap="sm">
                  <ThemeIcon size="lg" variant="light">
                    <Foot size={24} />
                  </ThemeIcon>
                  <Title order={4}>Foot Elevation</Title>
                </Group>
                <Badge size="lg">{footElevation}°</Badge>
              </Group>
            </Card>
          </Stack>
        </Grid.Col>

        <Grid.Col span={12}>
          <Card withBorder radius="md" p="xl">
            <Title order={4} mb="md">Event Log</Title>
            <Stack gap="xs">
              <Text>Last Detected Change: {lastChange}</Text>
              <Text>Auto Response Triggered: {autoResponse}</Text>
            </Stack>
          </Card>
        </Grid.Col>
      </Grid>
    </Box>
  );
}
