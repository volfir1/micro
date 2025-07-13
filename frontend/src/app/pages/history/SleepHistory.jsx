import { useState } from 'react';
import {
  Box,
  Title,
  Text,
  Stack,
  Group,
  Button,
  Card,
  Table,
  Badge,
  Modal,
  ScrollArea,
  Grid
} from '@mantine/core';
import { DatePickerInput } from '@mantine/dates';
import { LineChart, BarChart } from '@mantine/charts';
import { useDisclosure } from '@mantine/hooks';
import { sleepSessions, sleepQualityData, heartRateAvgData, triggerLogs } from './data';

export default function SleepHistory() {
  const [selectedSession, setSelectedSession] = useState(null);
  const [opened, { open, close }] = useDisclosure(false);

  const handleRowClick = (session) => {
    setSelectedSession(session);
    open();
  };

  const rows = sleepSessions.map((session) => (
    <Table.Tr key={session.id} onClick={() => handleRowClick(session)} style={{ cursor: 'pointer' }}>
      <Table.Td>{session.date}</Table.Td>
      <Table.Td>{session.duration}</Table.Td>
      <Table.Td>{session.sleepScore}%</Table.Td>
      <Table.Td>{session.snoreEvents}</Table.Td>
      <Table.Td>{session.avgHR} BPM</Table.Td>
      <Table.Td>
        <Badge color={session.status === 'Good' ? 'green' : 'orange'}>
          {session.status}
        </Badge>
      </Table.Td>
    </Table.Tr>
  ));

  return (
    <Box p="xl">
      <Stack gap="xs" mb="xl">
        <Title order={2}>Sleep History</Title>
        <Text c="dimmed">Review your past sleep sessions and analytics.</Text>
      </Stack>

      <Group justify="space-between" mb="xl">
        <DatePickerInput type="range" placeholder="Filter by Date Range" />
        <Group>
          <Button variant="default">Export CSV</Button>
          <Button variant="default">Export PDF</Button>
          <Button variant="default">Export JSON</Button>
        </Group>
      </Group>

      <Card withBorder radius="md" p="xl" mb="xl">
        <Title order={4} mb="md">Sleep Sessions</Title>
        <ScrollArea h={300}>
          <Table highlightOnHover withTableBorder withColumnBorders>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Date</Table.Th>
                <Table.Th>Duration</Table.Th>
                <Table.Th>Score</Table.Th>
                <Table.Th>Events</Table.Th>
                <Table.Th>Avg HR</Table.Th>
                <Table.Th>Status</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>{rows}</Table.Tbody>
          </Table>
        </ScrollArea>
      </Card>

      <Grid gutter="xl" mb="xl">
        <Grid.Col span={{ base: 12, md: 6 }}>
          <Card withBorder radius="md" p="xl" h="100%">
            <Title order={4} mb="md">Sleep Quality Over Time</Title>
            <LineChart
              h={250}
              data={sleepQualityData}
              dataKey="date"
              series={[
                { name: 'score', label: 'Sleep Score', color: 'blue' },
                { name: 'snoreCount', label: 'Snore Events', color: 'red' },
              ]}
            />
          </Card>
        </Grid.Col>
        <Grid.Col span={{ base: 12, md: 6 }}>
          <Card withBorder radius="md" p="xl" h="100%">
            <Title order={4} mb="md">Average Heart Rate Per Session</Title>
            <BarChart
              h={250}
              data={heartRateAvgData}
              dataKey="date"
              series={[{ name: 'avgHR', label: 'Avg HR', color: 'pink' }]}
            />
          </Card>
        </Grid.Col>
      </Grid>

      <Card withBorder radius="md" p="xl">
        <Title order={4} mb="md">Trigger Logs</Title>
        <Table highlightOnHover withTableBorder withColumnBorders>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>Timestamp</Table.Th>
              <Table.Th>Action</Table.Th>
              <Table.Th>Reason</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {triggerLogs.map((log, index) => (
              <Table.Tr key={index}>
                <Table.Td>{log.timestamp}</Table.Td>
                <Table.Td>{log.action}</Table.Td>
                <Table.Td>{log.reason}</Table.Td>
              </Table.Tr>
            ))}
          </Table.Tbody>
        </Table>
      </Card>

      <Modal opened={opened} onClose={close} title="Session Details" size="lg">
        {selectedSession && (
          <Stack>
            <Text><b>Date:</b> {selectedSession.date}</Text>
            <Text><b>Duration:</b> {selectedSession.duration}</Text>
            <Text><b>Sleep Score:</b> {selectedSession.sleepScore}%</Text>
            <Text><b>Snore Events:</b> {selectedSession.snoreEvents}</Text>
            <Text><b>Average Heart Rate:</b> {selectedSession.avgHR} BPM</Text>
            <Text><b>Status:</b> {selectedSession.status}</Text>
            {/* Add more detailed graphs/info here if needed */}
          </Stack>
        )}
      </Modal>
    </Box>
  );
}