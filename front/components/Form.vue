<template>
    <div v-if="tripOptions">
        <div v-if="tripOptions.departures.length > 1 || tripOptions.arrivals.length > 1" class="flex items-center space-x-4">
            <p class="text-sm text-muted-foreground">Departure</p>
            <DepartureArrival :options="tripOptions.departures"/>

            <p class="text-sm text-muted-foreground">Arrival</p>
            <DepartureArrival :options="tripOptions.arrivals"/>
        </div>
        <div v-else class="flex items-center space-x-4">
            <p class="text-sm text-muted-foreground">Departure</p>
            <Badge> {{ tripOptions.departures[0] }}</Badge>

            <p class="text-sm text-muted-foreground">Arrival</p>
            <Badge>{{ tripOptions.arrivals[0] }}</Badge>
        </div>

        <Button>Save</Button>
    </div>
</template>

<script setup lang="ts">
import type { PropType } from 'vue';
import DepartureArrival from './DepartureArrival.vue';
import type { TripOptionsResponse } from '~/types';

const props = defineProps({
    tripOptions: {
        type: Object as PropType<TripOptionsResponse>,
        required: true,
    },
});
</script>