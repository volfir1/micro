import { useState } from 'react';
import {
  IconDatabaseImport,
  IconFingerprint,
  IconKey,
  IconLogout,
  IconSettings,
  IconSwitchHorizontal,
} from '@tabler/icons-react';
import { MdSpaceDashboard } from "react-icons/md";
import { FaDatabase } from "react-icons/fa";
import { GiNightSleep } from "react-icons/gi";
import { Avatar, Code, Group, Stack, Text } from '@mantine/core';
import classes from './sidebar.module.css';
import {Link} from 'react-router';

const data = [
  { link: '/dashboard', label: 'Dashboard', icon: MdSpaceDashboard },
  { link: '/livedata', label: 'Live Data', icon: FaDatabase },
  { link: '/posture', label: 'Posture & Position', icon: IconFingerprint },
  { link: '/controls', label: 'Device Controls', icon: IconKey },
  { link: '/history', label: 'Sleep History', icon: GiNightSleep},
  { link: '/settings', label: 'System Settings', icon: IconSettings },
];

export function Sidebar() {
  const [active, setActive] = useState('Billing');

  const links = data.map((item) => (
    <Link
      to={item.link}
      className={classes.link}
      data-active={item.label === active || undefined}
      key={item.label}
      onClick={() => {
        setActive(item.label);
      }}
    >
      <item.icon className={classes.linkIcon} stroke={1.5} />
      <span>{item.label}</span>
    </Link>
  ));

  return (
    <nav className={classes.navbar}>
      <div className={classes.navbarMain}>
        <Group className={classes.header} justify="space-between">
          <Code fw={700} className={classes.version}>
            Micricontroller
          </Code>
        </Group>
        <Group my="md" wrap="nowrap" ml='l' pb='md' pl='md'>
          <Avatar color="cyan" radius="xl">LS</Avatar>
          <Stack gap={0}>
            <Text fw={500} c={'white'}>Welcome Lester</Text>
            <Text c="dimmed" size="sm">lester@example.com</Text>
          </Stack>
        </Group>
        {links}
      </div>

      <div className={classes.footer}>
        <a href="#" className={classes.link} onClick={(event) => event.preventDefault()}>
          <IconSwitchHorizontal className={classes.linkIcon} stroke={1.5} />
          <span>Change account</span>
        </a>

        <a href="#" className={classes.link} onClick={(event) => event.preventDefault()}>
          <IconLogout className={classes.linkIcon} stroke={1.5} />
          <span>Logout</span>
        </a>
      </div>
    </nav>
  );
}