import { TextInput, PasswordInput, Button, Paper, Title, Text, Anchor, Center, Box } from '@mantine/core';
import { useForm } from '@mantine/form';
import { Link } from "react-router";
export default function Signup() {
  const form = useForm({
    initialValues: {
      email: '',
      password: '',
      confirmPassword: '',
    },

    validate: {
      email: (val) => (/^\S+@\S+$/.test(val) ? null : 'Invalid email'),
      password: (val) => (val.length >= 6 ? null : 'Password should include at least 6 characters'),
      confirmPassword: (val, values) =>
        val === values.password ? null : 'Passwords did not match',
    },
  });

  return (
    <Center
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(45deg, #673AB7 0%, #3F51B5 100%)',
      }}
    >
      <Paper withBorder shadow="md" p={30} mt={30} radius="md" style={{ width: 400 }}>
        <Title order={2} ta="center" mt="md" mb={50}>
          Create your account
        </Title>
        <TextInput
          label="Email"
          placeholder="you@mantine.dev"
          required
          {...form.getInputProps('email')}
        />
        <PasswordInput
          label="Password"
          placeholder="Your password"
          required
          mt="md"
          {...form.getInputProps('password')}
        />
        <PasswordInput
          label="Confirm Password"
          placeholder="Confirm your password"
          required
          mt="md"
          {...form.getInputProps('confirmPassword')}
        />
        <Button fullWidth mt="xl">
          Sign up
        </Button>
        <Text ta="center" mt="md">
          Already have an account?{' '}
          <Anchor component={Link} to='/login' type="button" size="xs">
            Sign in
          </Anchor>
        </Text>
      </Paper>
    </Center>
  );
}