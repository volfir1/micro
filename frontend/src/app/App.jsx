import { Box } from "@mantine/core";
import { Route, Routes } from "react-router";
import MainLayout from "./layout/MainLayout";
import Dashboard from "./pages/dashboard/Dashboard";
import LiveData from "./pages/livedata/LiveData";
import DeviceControls from './pages/controls/DeviceControls';
import Position from './pages/posture/Posture';
import SleepHistory from "./pages/history/SleepHistory";
import Login from "./(auth)/login/Login";
import Signup from "./(auth)/signup/Signup";
import SystemSettings from "./pages/settings/SystemSettings";
function App() {
  return (
    <>
      <div>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/" element={<MainLayout />}>
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="/livedata" element={<LiveData />} />
            <Route path="/controls" element={<DeviceControls />} />
            <Route path="/posture" element={<Position />} />
            <Route path="/history" element={<SleepHistory />} />  
            <Route path="/settings" element={<SystemSettings />} />
          </Route>
        </Routes>
      </div>
    </>
  );
}

export default App;
