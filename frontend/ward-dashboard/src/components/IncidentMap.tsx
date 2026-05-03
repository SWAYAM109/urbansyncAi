import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { useIncidents } from '../context/IncidentContext';

// Fix for default Leaflet icon issues in React
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom icons based on priority
const createCustomIcon = (color: string) => {
  return new L.DivIcon({
    className: 'custom-leaflet-icon',
    html: `<div style="background-color: ${color}; width: 16px; height: 16px; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 10px rgba(0,0,0,0.5);"></div>`,
    iconSize: [16, 16],
    iconAnchor: [8, 8],
  });
};

const highPriorityIcon = createCustomIcon('#ef4444'); // red-500
const mediumPriorityIcon = createCustomIcon('#eab308'); // yellow-500
const lowPriorityIcon = createCustomIcon('#3b82f6'); // blue-500
const resolvedIcon = createCustomIcon('#10b981'); // emerald-500

export const IncidentMap: React.FC = () => {
  const { incidents } = useIncidents();
  // Center roughly on Mumbai
  const center: [number, number] = [19.0760, 72.8777];

  return (
    <div className="w-3/4 h-screen bg-slate-900 relative">
      <MapContainer 
        center={center} 
        zoom={12} 
        style={{ height: '100%', width: '100%' }}
        zoomControl={false}
      >
        {/* Dark theme tiles */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        />
        
        {incidents.map((incident) => {
          const icon = incident.status === 'Resolved'
            ? resolvedIcon
            : incident.priority === 'High' 
              ? highPriorityIcon 
              : incident.priority === 'Medium' 
                ? mediumPriorityIcon 
                : lowPriorityIcon;

          return (
            <Marker 
              key={incident.id} 
              position={incident.coordinates}
              icon={icon}
            >
              <Popup className="custom-popup">
                <div className="p-1">
                  <div className="font-bold text-slate-800 mb-1">{incident.type}</div>
                  <div className="text-sm text-slate-600 mb-2">{incident.address}</div>
                  <div className="flex gap-2">
                    <span className="px-2 py-1 bg-slate-100 rounded text-xs font-semibold text-slate-700">
                      {incident.status}
                    </span>
                    <span className="px-2 py-1 bg-blue-50 text-blue-700 rounded text-xs font-semibold">
                      {incident.assigned_agents.join(', ')}
                    </span>
                  </div>
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
      
      {/* Decorative gradient overlay for map edges */}
      <div className="absolute inset-0 pointer-events-none shadow-[inset_0_0_100px_rgba(15,23,42,0.8)] z-[400]" />
    </div>
  );
};
