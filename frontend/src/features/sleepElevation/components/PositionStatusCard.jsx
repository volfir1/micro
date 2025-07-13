import { Card, Group, Title, Badge, ThemeIcon } from '@mantine/core';
import { AppIcons } from '@/shared/components/icons/AppIcons';

export function PositionStatusCard({ position }) {
  const { Position } = AppIcons;
  
  return (
    <Card withBorder radius="md" p="xl">
      <Group justify="space-between">
        <Group gap="sm">
          <ThemeIcon size="lg" variant="light">
            <Position size={24} />
          </ThemeIcon>
          <Title order={4}>Current Position</Title>
        </Group>
        <Badge size="lg">{position}</Badge>
      </Group>
    </Card>
  );
}