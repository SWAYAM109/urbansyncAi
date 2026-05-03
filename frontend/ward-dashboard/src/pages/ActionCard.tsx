import React, { useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { ChevronLeft, Navigation, MapPin, AlertTriangle, CheckCircle2 } from 'lucide-react';
import { useIncidents } from '../context/IncidentContext';

const sopSteps = [
  { id: 'step1', text: 'Secure the perimeter & place traffic cones.' },
  { id: 'step2', text: 'Shut off the sector water valve.' },
  { id: 'step3', text: 'Excavate and patch the pipeline.' },
  { id: 'step4', text: 'Restore pressure and verify no leaks.' },
];

export const ActionCard: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { incidents, resolveIncident } = useIncidents();
  const [checkedSteps, setCheckedSteps] = useState<Record<string, boolean>>({});

  const incident = incidents.find(inc => inc.id === id);

  if (!incident) {
    return (
      <div className="max-w-md mx-auto min-h-screen bg-slate-900 flex flex-col items-center justify-center text-slate-200">
        <AlertTriangle size={48} className="text-slate-500 mb-4" />
        <h2 className="text-xl font-bold">Incident Not Found</h2>
        <Link to="/" className="mt-4 text-primary underline">Return to Dashboard</Link>
      </div>
    );
  }

  const handleToggleStep = (stepId: string) => {
    setCheckedSteps(prev => ({
      ...prev,
      [stepId]: !prev[stepId]
    }));
  };

  const isAllChecked = sopSteps.every(step => checkedSteps[step.id]);

  const handleComplete = () => {
    if (id) {
      resolveIncident(id);
      navigate('/');
    }
  };

  return (
    <div className="max-w-md mx-auto min-h-screen bg-slate-900 shadow-2xl relative pb-24 font-sans text-slate-200">
      
      {/* Header Section */}
      <header className="bg-slate-800/80 backdrop-blur-md sticky top-0 z-10 border-b border-slate-700/50">
        <div className="flex items-center px-4 py-3">
          <Link 
            to="/" 
            className="flex items-center justify-center w-11 h-11 rounded-full bg-slate-700/50 hover:bg-slate-600/50 text-slate-300 transition-colors"
          >
            <ChevronLeft size={24} />
          </Link>
          <div className="ml-3 flex-1">
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Incident #{incident.id}</p>
            <h1 className="text-xl font-bold text-slate-100 leading-tight">{incident.type}</h1>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="p-4 space-y-6">
        
        {/* Priority & Status Row */}
        <div className="flex items-center justify-between">
          <div className={`flex items-center gap-2 border px-3 py-1.5 rounded-lg font-semibold ${
            incident.priority === 'High' ? 'bg-red-500/10 border-red-500/20 text-red-400' :
            incident.priority === 'Medium' ? 'bg-yellow-500/10 border-yellow-500/20 text-yellow-400' :
            'bg-blue-500/10 border-blue-500/20 text-blue-400'
          }`}>
            <AlertTriangle size={18} />
            <span>Priority {incident.priority === 'High' ? '1' : incident.priority === 'Medium' ? '2' : '3'}</span>
          </div>
          <div className={`border px-3 py-1.5 rounded-lg font-semibold text-sm ${
            incident.status === 'Resolved' ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' :
            incident.status === 'Resolving' ? 'bg-yellow-500/10 border-yellow-500/20 text-yellow-400' :
            'bg-red-500/10 border-red-500/20 text-red-400'
          }`}>
            {incident.status}
          </div>
        </div>

        {/* Location Block */}
        <div className="bg-slate-800 border border-slate-700/50 rounded-2xl p-5 shadow-lg">
          <div className="flex items-start gap-3">
            <div className="bg-primary/20 p-2.5 rounded-full text-primary">
              <MapPin size={24} />
            </div>
            <div className="flex-1">
              <h2 className="text-lg font-bold text-slate-100">{incident.address}</h2>
              <p className="text-slate-400 text-sm mt-1">SLA: {incident.sla_timer}</p>
            </div>
          </div>
          <button className="w-full mt-4 flex items-center justify-center gap-2 bg-primary/10 hover:bg-primary/20 text-primary border border-primary/30 rounded-xl py-3.5 font-semibold transition-colors min-h-[48px]">
            <Navigation size={20} />
            Get Directions
          </button>
        </div>

        {/* SOP Checklist */}
        <div>
          <h3 className="text-lg font-bold text-slate-100 mb-4 px-1 flex items-center gap-2">
            <CheckCircle2 className="text-accent" />
            Standard Operating Procedure
          </h3>
          <div className="space-y-3">
            {sopSteps.map((step, index) => (
              <label 
                key={step.id} 
                className={`flex items-start gap-4 p-4 rounded-2xl border transition-all cursor-pointer min-h-[64px] ${
                  checkedSteps[step.id] 
                    ? 'bg-accent/10 border-accent/30 opacity-70' 
                    : 'bg-slate-800 border-slate-700/50 hover:bg-slate-700/50'
                }`}
              >
                <div className="relative flex items-center justify-center mt-0.5">
                  <input
                    type="checkbox"
                    className="w-7 h-7 rounded-md border-2 border-slate-500 bg-slate-900 appearance-none checked:bg-accent checked:border-accent transition-all cursor-pointer"
                    checked={checkedSteps[step.id] || false}
                    onChange={() => handleToggleStep(step.id)}
                  />
                  {checkedSteps[step.id] && (
                    <CheckCircle2 size={20} className="absolute text-slate-900 pointer-events-none" />
                  )}
                </div>
                <div className="flex-1">
                  <p className={`text-base font-medium transition-colors ${checkedSteps[step.id] ? 'text-slate-400 line-through decoration-slate-500' : 'text-slate-200'}`}>
                    <span className="font-bold text-slate-500 mr-2">{index + 1}.</span>
                    {step.text}
                  </p>
                </div>
              </label>
            ))}
          </div>
        </div>
      </main>

      {/* Sticky Footer */}
      <footer className="fixed bottom-0 left-0 right-0 w-full max-w-md mx-auto bg-slate-900/95 backdrop-blur-xl border-t border-slate-700/50 p-4 shadow-[0_-10px_40px_rgba(0,0,0,0.5)] z-20">
        <button 
          disabled={!isAllChecked}
          onClick={handleComplete}
          className={`w-full min-h-[56px] rounded-2xl text-lg font-bold transition-all shadow-lg flex items-center justify-center gap-2 ${
            isAllChecked 
              ? 'bg-accent hover:bg-emerald-400 text-slate-900 translate-y-0 opacity-100 shadow-accent/25' 
              : 'bg-slate-700 text-slate-500 cursor-not-allowed opacity-70'
          }`}
        >
          {isAllChecked && <CheckCircle2 size={22} />}
          {isAllChecked ? 'Mark Incident as Complete' : 'Complete SOP to Proceed'}
        </button>
      </footer>
    </div>
  );
};
