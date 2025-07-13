import {
  Box,
  Card,
  Group,
  Title,
  Badge,
  Text,
  Grid,
  Stack,
} from "@mantine/core";
import { AppIcons } from "@/shared/components/icons/AppIcons";
import {
  SleepMonitor,
  HeartRateCard,
  SnoreDetection,
  BodyWeight,
  NeckAngle
} from "@/features/features";

export default function Dashboard() {
  

  return (
    <Box p="xl">
      <Stack gap="xs" mb="xl">
        <Title order={2}>Sleep Monitoring Dashboard</Title>
        <Text c="dimmed">Welcome to your dashboard!</Text>
      </Stack>
      {/* Sleep Monitor */}
      <Grid gutter="xl">
        <Grid.Col span={{ base: 12, md: 6, lg: 4 }}>
          <SleepMonitor />
        </Grid.Col>
        {/* Heart Rate */}
        <Grid.Col span={{ base: 12, md: 6, lg: 4 }}>
          <HeartRateCard />
        </Grid.Col>
        {/* Snore Detection */}
        <Grid.Col span={{ base: 12, md: 6, lg: 4 }}>
          <SnoreDetection />
        </Grid.Col>
        {/* Body Weight */}
        <Grid.Col span={{ base: 12, md: 6, lg: 4 }}>
          <BodyWeight />
        </Grid.Col>
        {/* Sleep Position */}
        <Grid.Col span={{ base: 12, md: 6, lg: 4 }}>
          <NeckAngle />
        </Grid.Col>
      </Grid>
    </Box>
  );
}
