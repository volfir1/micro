import { useEffect } from 'react';
import { Card, Group, Stack, Text, Title } from '@mantine/core';
import { AppIcons } from '@/shared/components/icons/AppIcons';
import { useGyroscopeData } from '@/features/neckAdjust/hooks/gyro/useGyroscopeData';
import { usePillowAdjustment } from '@/features/neckAdjust/hooks/servo/usePillowAdjustment';

export function NeckAngle() {
  const { Position } = AppIcons;
  const { pitch, roll } = useGyroscopeData();
  const { adjustPillow } = usePillowAdjustment();

  useEffect(() => {
    const pitchThreshold = 15;
    const rollThreshold = 15;

    if (Math.abs(pitch) > pitchThreshold || Math.abs(roll) > rollThreshold) {
      const avgAngle = (pitch + roll) / 2;
      adjustPillow(avgAngle);
    }
  }, [pitch, roll]);

  return (
    <Card withBorder radius="md" p="xl" h="100%">
      <Stack gap="md">
        <Group gap="sm">
          <Position size={28} color="pink" />
          <Title order={4}>Neck Angle</Title>
        </Group>
        <Stack gap="xs">
          <Group justify="space-between">
            <Text size="sm">Pitch:</Text>
            <Text size="sm">{pitch !== undefined ? pitch.toFixed(1) : '...'}</Text>
          </Group>
          <Group justify="space-between">
            <Text size="sm">Roll:</Text>
            <Text size="sm">{roll !== undefined ? roll.toFixed(1) : '...'}</Text>
          </Group>
        </Stack>
      </Stack>
    </Card>
  );
}
