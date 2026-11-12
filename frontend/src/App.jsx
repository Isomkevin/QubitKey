import { Route, Routes } from "react-router-dom";
import Layout from "./components/Layout.jsx";
import OverviewPage from "./pages/OverviewPage.jsx";
import LabPage from "./pages/LabPage.jsx";
import ObservatoryPage from "./pages/ObservatoryPage.jsx";
import AuthenticatorPage from "./pages/AuthenticatorPage.jsx";
import PqcPage from "./pages/PqcPage.jsx";
import AboutPage from "./pages/AboutPage.jsx";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<OverviewPage />} />
        <Route path="lab" element={<LabPage />} />
        <Route path="observatory" element={<ObservatoryPage />} />
        <Route path="authenticator" element={<AuthenticatorPage />} />
        <Route path="pqc" element={<PqcPage />} />
        <Route path="about" element={<AboutPage />} />
      </Route>
    </Routes>
  );
}
