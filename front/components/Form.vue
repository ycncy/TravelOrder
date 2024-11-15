<template>
    <div v-if="tripOptions">
        <div class="flex items-center space-x-4">
            <template v-for="(options, label) in displayOptions" :key="label">
                <p class="text-sm text-muted-foreground">{{ label }}</p>
                <template v-if="options.length > 1">
                    <DepartureArrival :options="options" />
                </template>
                <template v-else>
                    <Badge>{{ options[0] }}</Badge>
                </template>
            </template>
        </div>

        <!-- <Button>Save</Button> -->
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

const displayOptions = computed(() => ({
    Departure: props.tripOptions.departures || [],
    Arrival: props.tripOptions.arrivals || []
}));
</script>