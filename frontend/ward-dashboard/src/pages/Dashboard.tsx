import React from 'react';
import { Sidebar } from '../components/Sidebar';
import { IncidentMap } from '../components/IncidentMap';

export const Dashboard: React.FC = () => {
  return (
    <div className="flex h-screen w-screen overflow-hidden bg-background">
      <Sidebar />
      <IncidentMap />
    </div>
  );
};
