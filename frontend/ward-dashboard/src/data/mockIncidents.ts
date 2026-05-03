export type IncidentStatus = 'Active' | 'Resolving' | 'Resolved';
export type IncidentPriority = 'High' | 'Medium' | 'Low';

export interface Incident {
  id: string;
  type: string;
  status: IncidentStatus;
  coordinates: [number, number]; // [lat, lng]
  priority: IncidentPriority;
  assigned_agents: string[];
  sla_timer: string; // e.g., "15m left"
  address: string;
}

export const mockIncidents: Incident[] = [
  {
    id: "INC-001",
    type: "Major Pipe Burst",
    status: "Active",
    coordinates: [19.0760, 72.8777], // Mumbai coordinates
    priority: "High",
    assigned_agents: ["Water", "Traffic"],
    sla_timer: "15m left",
    address: "LBS Marg, Kurla West",
  },
  {
    id: "INC-002",
    type: "Traffic Signal Failure",
    status: "Resolving",
    coordinates: [19.0820, 72.8810],
    priority: "Medium",
    assigned_agents: ["Traffic"],
    sla_timer: "45m left",
    address: "BKC Junction",
  },
  {
    id: "INC-003",
    type: "Transformer Sparking",
    status: "Active",
    coordinates: [19.0650, 72.8650],
    priority: "High",
    assigned_agents: ["Power"],
    sla_timer: "10m left",
    address: "Sion Circle",
  },
  {
    id: "INC-004",
    type: "Deep Pothole",
    status: "Active",
    coordinates: [19.0900, 72.8550],
    priority: "Low",
    assigned_agents: ["Roads"],
    sla_timer: "2h left",
    address: "Mahim Causeway",
  },
  {
    id: "INC-005",
    type: "Fallen Tree",
    status: "Resolving",
    coordinates: [19.0700, 72.8900],
    priority: "Medium",
    assigned_agents: ["Parks", "Traffic"],
    sla_timer: "30m left",
    address: "Chembur Naka",
  }
];
