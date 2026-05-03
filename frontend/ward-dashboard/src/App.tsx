import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Dashboard } from './pages/Dashboard';
import { ActionCard } from './pages/ActionCard';
import { IncidentProvider } from './context/IncidentContext';

function App() {
  return (
    <IncidentProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/action-card/:id" element={<ActionCard />} />
        </Routes>
      </BrowserRouter>
    </IncidentProvider>
  );
}

export default App;
