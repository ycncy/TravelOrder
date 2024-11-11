import type { TripResponse, TripOptionsResponse } from "~/types";

const BASE_URL = "http://localhost:8000";

export const apiService = {
  async getShortestTrip(
    departureCity: string,
    arrivalCity: string
  ): Promise<TripResponse> {
    const response = await fetch(
      `${BASE_URL}/shortest-trip?departure_city=${encodeURIComponent(
        departureCity
      )}&arrival_city=${encodeURIComponent(arrivalCity)}`
    );
    if (!response.ok) {
      throw new Error(`Error fetching shortest trip: ${response.statusText}`);
    }
    return response.json();
  },

  async getTripOptions(
    sentence: string,
    model: string
  ): Promise<TripOptionsResponse> {
    const response = await fetch(
      `${BASE_URL}/trip-options?sentence=${encodeURIComponent(
        sentence
      )}&model=${encodeURIComponent(model)}`
    );
    if (!response.ok) {
      throw new Error(`Error fetching trip options: ${response.statusText}`);
    }
    return response.json();
  },
};
