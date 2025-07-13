import { Card, Group, Stack, Text, Title, Badge } from "@mantine/core";
import { AppIcons } from "@/shared/components/icons/AppIcons";
import { useBodyWeight } from "@/features/weightLCD/hooks/weight/useBodyWeight";

export function BodyWeight() {
  const { Weight } = AppIcons;
  const { weight } = useBodyWeight();

  const isInBed = weight > 30;

  return (
    <Card withBorder radius="md" p="xl" h="100%">
      <Stack gap="md" align="center">
        <Group gap="sm">
          <Weight size={28} color="gray" />
          <Title order={4}>Body Pressure</Title>
        </Group>
        <Text size="4rem" fw={700}>
          {weight} kg
        </Text>
        <Badge color={isInBed ? "blue" : "gray"} variant="light">
          {isInBed ? "Person in bed" : "Bed is empty"}
        </Badge>
      </Stack>
    </Card>
  );
}
