import React, { createContext, useState, useContext, ReactNode } from 'react';
import { Incident, mockIncidents as initialIncidents } from '../data/mockIncidents';

interface IncidentContextType {
  incidents: Incident[];
  resolveIncident: (id: string) => void;
}

const IncidentContext = createContext<IncidentContextType | undefined>(undefined);

export const IncidentProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [incidents, setIncidents] = useState<Incident[]>(initialIncidents);

  const resolveIncident = (id: string) => {
    setIncidents(prev => prev.map(incident => 
      incident.id === id ? { ...incident, status: 'Resolved' } : incident
    ));
  };

  return (
    <IncidentContext.Provider value={{ incidents, resolveIncident }}>
      {children}
    </IncidentContext.Provider>
  );
};

export const useIncidents = () => {
  const context = useContext(IncidentContext);
  if (context === undefined) {
    throw new Error('useIncidents must be used within an IncidentProvider');
  }
  return context;
};
