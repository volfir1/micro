import { useEffect } from "react";
import { Card, Stack, Group, Title, Text, Badge, Alert } from "@mantine/core";
import { AppIcons } from "@/shared/components/icons/AppIcons";
import { useHeartRateData } from "@/features/heartFan/hooks/heart/useHeartRateData";
import { useFanControl } from "@/features/heartFan/hooks/relay/useFanControl";
import { useSystemState } from '@/features/useSystemState';


export function HeartRateCard() {
  const { Heart, AlertCircle } = AppIcons;
  const { rate, status, isConnected } = useHeartRateData();
  const { isInBed } = useSystemState();
  const { turnFan } = useFanControl();

  useEffect(() => {
    if (rate > 100) {
      turnFan(true);
    } else {
      turnFan(false);
    }
  }, [rate]);

  // Show "waiting" state when nobody is in bed
  if (!isInBed) {
    return (
      <Card withBorder radius="md" p="xl" h="100%">
        <Stack gap="md" align="center">
          <Group gap="sm">
            <Heart size={28} color="gray" />
            <Title order={4}>Heart Rate</Title>
          </Group>
          <Text c="dimmed" fs="italic">Waiting for person</Text>
          <Badge color="gray" variant="light">Not Monitoring</Badge>
        </Stack>
      </Card>
    );
  }

  // Show error state if sensor not connected
  if (!isConnected) {
    return (
      <Card withBorder radius="md" p="xl" h="100%">
        <Stack gap="md">
          <Group gap="sm">
            <Heart size={28} color="red" />
            <Title order={4}>Heart Rate</Title>
          </Group>
          <Alert icon={<AlertCircle size={16} />} title="Connection Error" color="red">
            Unable to connect to heart rate monitor
          </Alert>
        </Stack>
      </Card>
    );
  }

  // Normal state with data
  return (
    <Card withBorder radius="md" p="xl" h="100%">
      <Stack gap="md" align="center">
        <Group gap="sm">
          <Heart size={28} color="red" />
          <Title order={4}>Heart Rate</Title>
        </Group>
        <Text size="4rem" fw={700}>
          {rate}
        </Text>
        <Badge color={status === "Normal" ? "green" : "red"} variant="light">
          BPM - {status} Range
        </Badge>
      </Stack>
    </Card>
  );
}