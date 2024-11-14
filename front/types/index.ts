// Represents a single travel step in the shortest trip
export interface TripStep {
    departure_station: string;
    arrival_station: string;
    travel_time: number;
    departure_city: string;
    arrival_city: string;
    stop_lat_start: number;
    stop_lon_start: number;
    stop_lat_end: number;
    stop_lon_end: number;
  }
  
// Response for getShortestTrip API
export interface TripResponse {
    total_time: number;
    steps: TripStep[];
}

// Response for getTripOptions API
export interface TripOptionsResponse {
    departures: string[];
    arrivals: string[];
}

// AI Model types for getTripOptions API
export type AIModels = 'SPACY' | 'CAMEMBERT';