import React from 'react';
import { AlertCircle, Clock, MapPin, Users, CheckCircle2 } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useIncidents } from '../context/IncidentContext';

export const Sidebar: React.FC = () => {
  const { incidents } = useIncidents();
  return (
    <div className="w-1/4 h-screen bg-surface border-r border-slate-700/50 flex flex-col shadow-2xl z-10 relative">
      <div className="p-6 border-b border-slate-700/50 bg-slate-800/50 backdrop-blur-sm">
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
          <AlertCircle className="text-primary" />
          Ward Dashboard
        </h1>
        <p className="text-sm text-slate-400 mt-1">Real-time incident tracking</p>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {incidents.map((incident) => (
          <Link 
            to={`/action-card/${incident.id}`}
            key={incident.id} 
            className={`block bg-slate-800/40 border rounded-xl p-4 transition-all duration-200 cursor-pointer group shadow-lg ${
              incident.status === 'Resolved' 
                ? 'border-emerald-500/50 hover:bg-emerald-500/10' 
                : 'border-slate-700/50 hover:bg-slate-800/80 hover:border-slate-600'
            }`}
          >
            <div className="flex justify-between items-start mb-3">
              <span className={`px-2.5 py-1 text-xs font-semibold rounded-full border ${
                incident.status === 'Resolved'
                  ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                  : incident.status === 'Active' 
                    ? 'bg-red-500/10 text-red-400 border-red-500/20' 
                    : 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20'
              }`}>
                {incident.status}
              </span>
              <span className={`text-xs font-medium px-2 py-1 rounded bg-slate-700/50 ${
                incident.priority === 'High' ? 'text-red-400' : incident.priority === 'Medium' ? 'text-yellow-400' : 'text-blue-400'
              }`}>
                {incident.priority} Priority
              </span>
            </div>
            
            <h3 className="font-semibold text-slate-100 text-lg mb-1 group-hover:text-primary transition-colors">
              {incident.type}
            </h3>
            
            <div className="space-y-2 mt-4">
              <div className="flex items-center text-sm text-slate-400">
                <MapPin size={16} className="mr-2 text-slate-500" />
                <span className="truncate">{incident.address}</span>
              </div>
              
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center text-slate-400">
                  <Clock size={16} className="mr-2 text-slate-500" />
                  <span className={`font-mono ${incident.status === 'Resolved' ? 'line-through text-slate-600 decoration-emerald-500/50' : 'text-slate-300'}`}>
                    {incident.sla_timer}
                  </span>
                </div>
                
                <div className="flex items-center text-slate-400">
                  <Users size={16} className="mr-2 text-slate-500" />
                  <div className="flex gap-1">
                    {incident.assigned_agents.map(agent => (
                      <span key={agent} className="text-xs bg-slate-700/50 px-1.5 py-0.5 rounded text-slate-300">
                        {agent}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </Link>
        ))}
      </div>
      
      <div className="p-4 border-t border-slate-700/50 bg-slate-800/30 text-xs text-center text-slate-500">
        UrbanSync AI - Municipal Orchestration Platform
      </div>
    </div>
  );
};
