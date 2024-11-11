<template>
  <div>
    <BackButton></BackButton>

    <h2
      class="mt-10 scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight transition-colors first:mt-0"
    >
      Shortest Trip
    </h2>

    <div class="flex flex-col space-y-4 mt-5">
      <Input
        class="w-80"
        type="text"
        v-model="departureCity"
        placeholder="Departure"
      />
      <Input
        class="w-80"
        type="text"
        v-model="arrivalCity"
        placeholder="Arrival"
      />
      <Button @click="handleFetchTrip" class="w-20">Find</Button>
    </div>

    <div v-if="shortestTrip">
      <TripResultTable :trip="shortestTrip" />
      <h3>Result:</h3>
      <pre>{{ shortestTrip }}</pre>
    </div>
    <p v-else-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>
    <p v-else>Enter departure and arrival cities to find the shortest trip.</p>
  </div>
</template>

<script setup lang="ts">
import { useTrip } from '#build/imports';
import BackButton from '~/components/BackButton.vue';

const { fetchShortestTrip, shortestTrip, errorMessage } = useTrip();
const departureCity = ref('');
const arrivalCity = ref('');

const handleFetchTrip = () => {
  fetchShortestTrip(departureCity.value, arrivalCity.value);
}
</script>