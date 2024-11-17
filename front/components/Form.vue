<template>
    <div v-if="tripOptions">
        <div class="flex items-center space-x-4">
            <template v-for="(options, label) in displayOptions" :key="label">
                <p class="text-sm text-muted-foreground">{{ label }}</p>
                <template v-if="options.length > 1">
                    <DepartureArrival 
                        :options="options" 
                        @update:selected="label === 'Departure' ? selectedDeparture = $event : selectedArrival = $event"
                    />
                </template>
                <template v-else>
                    <Badge>{{ options[0] }}</Badge>
                </template>
            </template>
            <Button @click="handleFindShortestTrip">Find shortest trip</Button>
        </div>

        <div v-if="shortestTrip">
            <TripResultTable :trip="shortestTrip" />
        </div>
    </div>
</template>

<script setup lang="ts">
import type { PropType } from 'vue';
import DepartureArrival from './DepartureArrival.vue';
import type { TripOptionsResponse } from '~/types';
import { toast } from './ui/toast';

const { fetchShortestTrip, shortestTrip, errorMessage } = useTrip();

const props = defineProps({
    tripOptions: {
        type: Object as PropType<TripOptionsResponse>,
        required: true,
    },
});

const displayOptions = computed(() => ({
    Departure: props.tripOptions.departures || [],
    Arrival: props.tripOptions.arrivals || []
}));

const selectedDeparture = ref<string | null>(null);
const selectedArrival = ref<string | null>(null);

watchEffect(() => {
  if (displayOptions.value.Departure.length === 1) {
    selectedDeparture.value = displayOptions.value.Departure[0];
  }
  if (displayOptions.value.Arrival.length === 1) {
    selectedArrival.value = displayOptions.value.Arrival[0];
  }
});

const handleFindShortestTrip = () => {
    if (selectedDeparture.value && selectedArrival.value) {
        fetchShortestTrip(selectedDeparture.value, selectedArrival.value);
    } else {
        toast({
            title: 'Uh oh! Something went wrong.',
            description: errorMessage.value,
            variant: 'destructive',
        })
    }
}
</script>