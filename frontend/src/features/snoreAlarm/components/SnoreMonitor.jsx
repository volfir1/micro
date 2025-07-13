import { useEffect } from "react";
import {
  Card,
  Stack,
  Group,
  Title,
  Badge,
  Text,
  Progress,
} from "@mantine/core";
import { AppIcons } from "@/shared/components/icons/AppIcons";
import { useSleepMonitor } from "@/features/snoreAlarm/hooks/mic/useSnoreMonitor";
import { useLegElevation } from "@/features/sleepElevation/hooks/stepper/useLegElevation";

export function SleepMonitor() {
  const { Sleep } = AppIcons;
  const { duration, status, level } = useSleepMonitor();
  const { elevateLegs, lowerLegs } = useLegElevation();

  useEffect(() => {
    if (status === "Sleeping" && level > 85) {
      elevateLegs();
    } else {
      lowerLegs();
    }
  }, [status, level]);

  return (
    <Card withBorder radius="md" p="xl" h="100%">
      <Stack gap="md">
        <Group justify="space-between">
          <Group gap="sm">
            <Sleep size={28} color="violet" />
            <Title order={4}>Current Sleep Status</Title>
          </Group>
          <Badge color="lime">{status}</Badge>
        </Group>

        <Stack gap="xs">
          <Text size="sm">Snore Intensity</Text>
          <Progress value={level} color="violet" size="lg" radius="sm" />
          <Group justify="space-between">
            <Text size="sm">
              Sleep Duration:{" "}
              <Text span size="sm" fw={500}>
                {duration} Hour/s
              </Text>
            </Text>
            <Text size="xs" c="dimmed">
              {level}%
            </Text>
          </Group>
        </Stack>
      </Stack>
    </Card>
  );
}
