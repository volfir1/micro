
import { LineChart, BarChart } from "@mantine/charts";
import { Box, Stack, Title, Text, Group, Grid, Card, Badge } from "@mantine/core";
import { AppIcons } from "@/shared/components/icons/AppIcons";
import { heartRateData, breathingData } from "./data";
import { useHeartRateData } from "@/features/heartFan/hooks/heart/useHeartRateData";

const LiveData = () => {
  const { Heart, Breath, Snore, Weight, Position } = AppIcons;
  const {rate, status} = useHeartRateData();
  return (
    <Box p={20}>
      <Stack justify="center" align="center" mb={30}>
        <Title order={2}>Live Sleep Data</Title>
        <Text size="md" c="dimmed">
          Real-time monitoring and analysis
        </Text>
      </Stack>

      <Grid gutter="xl">
        <Grid.Col span={{ base: 12, md: 6, lg: 8 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Group justify="space-between" mb="xs">
                <Group>
                    <Heart size={24} color="red" />
                <Title order={3}>Heart Rate</Title>
              </Group>
              <Text size="xl" c="dimmed">    
                {rate} BPM {status}        
              </Text>
            </Group>
            <LineChart
              h={300}
              data={heartRateData}
              dataKey="time"
              series={[{ name: "Heart Rate", color: "red" }]}
              curveType="monotone"
            />
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, md: 6, lg: 4 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Group justify="space-between" mb="xs">
              <Group>
                <Breath size={24} />
                <Title order={3}>Breathing</Title>
              </Group>
              <Badge color="teal" size="lg">
                Normal
              </Badge>
            </Group>
            <BarChart
              h={300}
              data={breathingData}
              dataKey="time"
              series={[{ name: "Intensity", color: "teal.6" }]}
            />
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, md: 6, lg: 4 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Group justify="space-between" align="center">
              <Group>
                <Snore size={24} />
                <Title order={3}>Snoring</Title>
              </Group>
              <Badge color="red" size="lg">
                Detected
              </Badge>
            </Group>
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, md: 6, lg: 4 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Group justify="space-between" align="center">
              <Group>
                <Weight size={24} />
                <Title order={3}>Weight</Title>
              </Group>
              <Text size="xl">150 lbs</Text>
            </Group>
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, md: 6, lg: 4 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Group justify="space-between" align="center">
              <Group>
                <Position size={24} />
                <Title order={3}>Neck Angle</Title>
              </Group>
              <Text size="xl">15°</Text>
            </Group>
          </Card>
        </Grid.Col>

        <Grid.Col span={12}>
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Title order={3} mb="md">
              Sensor Health
            </Title>
            <Group justify="space-around">
              <Badge color="green" size="lg">
                Heart Rate: Online
              </Badge>
              <Badge color="green" size="lg">
                Breathing: Online
              </Badge>
              <Badge color="red" size="lg">
                Weight Sensor: Error
              </Badge>
              <Badge color="green" size="lg">
                Neck Angle: Online
              </Badge>
            </Group>
          </Card>
        </Grid.Col>
      </Grid>
    </Box>
  );
};

export default LiveData;
 