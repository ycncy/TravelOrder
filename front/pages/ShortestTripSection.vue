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

      <div class="flex gap-2">
        <Button @click="handleFetchTrip" class="w-20">Find</Button>
        <Button @click="clearInputAndResult" class="w-20" variant="outline">Clear</Button>
      </div>
    </div>

    <div v-if="shortestTrip">
      <TripResultTable :trip="shortestTrip" />
    </div>
    <p v-else>Enter departure and arrival cities to find the shortest trip.</p>
  </div>
</template>

<script setup lang="ts">
import { useTrip } from '#build/imports';
import BackButton from '~/components/BackButton.vue';
import { toast } from '@/components/ui/toast/use-toast';

const { fetchShortestTrip, shortestTrip, errorMessage } = useTrip();
const departureCity = ref('');
const arrivalCity = ref('');

const handleFetchTrip = () => {
  if (!departureCity.value || !arrivalCity.value) { 
    errorMessage.value = "Please provide both departure and arrival cities.";
    toast({
      title: 'Uh oh! Something went wrong.',
      description: errorMessage.value,
      variant: 'destructive',
    })
  }
  fetchShortestTrip(departureCity.value, arrivalCity.value);
}

const clearInputAndResult = () => {
  departureCity.value = '';
  arrivalCity.value = '';
  shortestTrip.value = null;
  errorMessage.value = '';
}
</script>