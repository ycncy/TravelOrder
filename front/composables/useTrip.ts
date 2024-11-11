import type { TripResponse, TripOptionsResponse } from "~/types";

export function useTrip() {
  const { $apiService } = useNuxtApp();
  const shortestTrip = ref<TripResponse | null>(null);
  const tripOptions = ref<TripOptionsResponse | null>(null);
  const errorMessage = ref("");

  const fetchShortestTrip = async (departureCity: string, arrivalCity: string) => {
    if (!departureCity || !arrivalCity) {
      errorMessage.value = "Please provide both departure and arrival cities.";
      return;
    }

    try {
      errorMessage.value = "";
      shortestTrip.value = await $apiService.getShortestTrip(departureCity, arrivalCity);
    } catch (error) {
      console.error("Failed to fetch shortest trip:", error);
      errorMessage.value = "Failed to fetch trip data. Please try again later.";
    }
  };

  const fetchTripOptions = async (sentence: string, model: string) => {
    if (!sentence || !model) {
      errorMessage.value = "Please provide both sentence describing your trip and the model you want to use";
    }

    try {
      errorMessage.value = "";
      tripOptions.value = await $apiService.getTripOptions(sentence, model);
    } catch (error) {
      console.error("Failed to fetch trip options:", error);
      errorMessage.value =
        "Failed to fetch trip options. Please try again later.";
    }
  };

  return {
    shortestTrip,
    tripOptions,
    errorMessage,
    fetchShortestTrip,
    fetchTripOptions,
  };
}
