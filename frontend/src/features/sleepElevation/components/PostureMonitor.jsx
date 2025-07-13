import { Card, Group, Stack, Text, Title, Badge, RingProgress, Grid } from "@mantine/core";
import { useGyroscopeData } from "@/features/neckAdjust/hooks/gyro/useGyroscopeData";
import { AppIcons } from "@/shared/components/icons/AppIcons";

export function PostureMonitor() {
    const {pitch, roll, isConnected, lastUpdated} = useGyroscopeData();
    const { Position } = AppIcons;


    const neckAngle = Math.abs(pitch)

    const getPostureStatus = () =>{
        if (neckAngle < 15) return "Good";
        if (neckAngle <  30 ) return "Poor"
        return "Bad";
    }

    const getPostureColor = () => {
        const status = getPostureStatus ()
        if (status === "Good") return "green";
        if (status === "Poor") return "yellow";
        return "red";
     }

     return(
          <Card withBorder radius="md" p="xl">
      <Stack gap="md">
        <Group justify="space-between">
          <Group gap="sm">
            <Position size={28} color="violet" />
            <Title order={4}>Neck Angle Monitor</Title>
          </Group>
          <Badge color={isConnected ? "green" : "red"}>
            {isConnected ? "Connected" : "Disconnected"}
          </Badge>
        </Group>

        <Grid>
          <Grid.Col span={6}>
            <RingProgress
              size={120}
              thickness={12}
              roundCaps
              sections={[{ value: (neckAngle / 45) * 100, color: getPostureColor() }]}
              label={
                <Stack gap={0} align="center">
                  <Text fw={700} ta="center" size="lg">
                    {neckAngle.toFixed(1)}°
                  </Text>
                  <Text size="xs">Neck Angle</Text>
                </Stack>
              }
            />
          </Grid.Col>
          
          <Grid.Col span={6}>
            <Stack gap="xs">
              <Group justify="space-between">
                <Text size="sm">Pitch:</Text>
                <Text fw={500}>{pitch}°</Text>
              </Group>
              
              <Group justify="space-between">
                <Text size="sm">Roll:</Text>
                <Text fw={500}>{roll}°</Text>
              </Group>
              
              <Group justify="space-between">
                <Text size="sm">Posture:</Text>
                <Badge color={getPostureColor()}>{getPostureStatus()}</Badge>
              </Group>
              
              <Text size="xs" c="dimmed" mt="sm">
                Last updated: {lastUpdated}
              </Text>
            </Stack>
          </Grid.Col>
        </Grid>
      </Stack>
    </Card>
     )
}
