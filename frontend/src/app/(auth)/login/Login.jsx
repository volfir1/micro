import {
  TextInput,
  PasswordInput,
  Button,
  Paper,
  Title,
  Text,
  Anchor,
  Center,
  Box,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { Link } from "react-router";
export default function Login() {
  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      email: "",
      password: "",
    },

    validate: {
      email: (val) => (/^\S+@\S+$/.test(val) ? null : "Invalid email"),
      password: (val) =>
        val.length >= 6
          ? null
          : "Password should include at least 6 characters",
    },
  });

  return (
    <form onSubmit={form.onSubmit((values)=> console.log(values))}>
    <Center
      style={{
        minHeight: "100vh",
        background: "linear-gradient(45deg, #673AB7 0%, #3F51B5 100%)",
      }}
    >
      <Paper
        withBorder
        shadow="md"
        p={30}
        mt={30}
        radius="md"
        style={{ width: 400 }}
      >
        <Title order={2} ta="center" mt="md" mb={50}>
          Welcome back!
        </Title>
        <TextInput
          label="Email"
          placeholder="you@gmail.com"
          required
          key={form.key('email')}
          {...form.getInputProps("email")}
        />
        <PasswordInput
          label="Password"
          placeholder="Your password"
          required
          mt="md"
          key={form.key('password')}
          {...form.getInputProps("password")}
        />
        <Button fullWidth mt="xl" type="submit">
          Sign in
        </Button>
        <Text ta="center" mt="md">
          Don't have an account yet?{" "}
          <Anchor component={Link} to="/signup" size="xs">
            Create account
          </Anchor>
        </Text>
      </Paper>
    </Center>
  </form>
  );
}
