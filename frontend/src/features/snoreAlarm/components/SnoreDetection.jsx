import { useEffect } from "react";
import { Card, Group, Stack, Text, Title, Badge } from "@mantine/core";
import { AppIcons } from "@/shared/components/icons/AppIcons";
import { useSnoreDetection } from "@/features/snoreAlarm/hooks/mic/useSnoreDetection";
import { useSpeakerControl } from "@/features/snoreAlarm/hooks/speaker/useSpeakerControl";

export function SnoreDetection() {
  const { Snore } = AppIcons;
  const { duration, lastDetected, frequency, isSnoring } = useSnoreDetection();
  const { playAlert } = useSpeakerControl();

  useEffect(() => {
    if (isSnoring) {
      playAlert("Mag relapse kana!!! Wake up!");
    }
  }, [isSnoring]);

  return (
    <Card withBorder radius="md" p="xl" h="100%">
      <Stack gap="md">
        <Group gap="sm">
          <Snore size={28} color="cyan" />
          <Title order={4}>Snore Detection</Title>
        </Group>
        <Stack gap="xs">
          <Group justify="space-between">
            <Text size="sm">Current Status:</Text>
            <Badge color={isSnoring ? "red" : "cyan"}>
              {isSnoring ? "Snoring Now" : duration}
            </Badge>
          </Group>
          <Group justify="space-between">
            <Text size="sm">Last Detected:</Text>
            <Text size="sm">{lastDetected}</Text>
          </Group>
          <Group justify="space-between">
            <Text size="sm">Frequency (1hr):</Text>
            <Text size="sm">{frequency}</Text>
          </Group>
        </Stack>
      </Stack>
    </Card>
  );
}
