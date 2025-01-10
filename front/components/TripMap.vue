<template>
    <div class="w-full h-full rounded-lg overflow-hidden border">
      <div v-if="isLoading" class="w-full h-full flex items-center justify-center bg-gray-100">
        Loading map...
      </div>
      <div ref="mapContainer" class="w-full h-full bg-red-100"></div>
    </div>
</template>
  
<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue'
import 'leaflet/dist/leaflet.css'
import type { TripStep } from '~/types';

const props = defineProps<{
    steps: TripStep[]  // Changed to accept array of steps
}>();

const mapContainer = ref<HTMLElement | null>(null)
const isLoading = ref(true)
let map: any = null
let markers: any[] = []
let polylines: any[] = []

async function initMap() {
    if (!mapContainer.value) return;

    const L = await import('leaflet');

    map = L.map(mapContainer.value).setView([48.8566, 2.3522], 5); // Default center (Paris)

    // L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(map);

    updateRoute();
    isLoading.value = false;
}

async function updateRoute() {
    if (!map) return;

    const L = await import('leaflet');

    // Clear existing markers and routes
    markers.forEach(marker => marker.remove());
    polylines.forEach(polyline => polyline.remove());
    markers = [];
    polylines = [];

    const allCoordinates: [number, number][] = [];

    if (props.steps.length === 0) return;

    const firstStep = props.steps[0];
    const lastStep = props.steps[props.steps.length - 1];

    const firstDepartureCoords: [number, number] = [firstStep.stop_lat_start, firstStep.stop_lon_start];
    const lastArrivalCoords: [number, number] = [lastStep.stop_lat_end, lastStep.stop_lon_end];

    allCoordinates.push(firstDepartureCoords);
    allCoordinates.push(lastArrivalCoords);

    const departureMarker = L.marker(firstDepartureCoords)
        .bindPopup(`<b>${firstStep.departure_city}</b><br>${firstStep.departure_station}<br>Start of Trip`)
        .addTo(map);
    markers.push(departureMarker);

    const arrivalMarker = L.marker(lastArrivalCoords)
        .bindPopup(`<b>${lastStep.arrival_city}</b><br>${lastStep.arrival_station}<br>Final Destination`)
        .addTo(map);
    markers.push(arrivalMarker);


    props.steps.forEach((step) => {
        const departureCoords: [number, number] = [step.stop_lat_start, step.stop_lon_start];
        const arrivalCoords: [number, number] = [step.stop_lat_end, step.stop_lon_end];

        const polyline = L.polyline([departureCoords, arrivalCoords], {
            color: '#2563eb',
            weight: 3,
            opacity: 0.7
        }).addTo(map);
        polylines.push(polyline);
    });

    // Fit map to show entire route
    if (allCoordinates.length > 0) {
    const bounds = L.latLngBounds(allCoordinates);
    map.fitBounds(bounds, { padding: [50, 50] });
    }
}

// Watch for changes in steps
watch(() => props.steps, () => {
    updateRoute();
}, { deep: true })

onMounted(() => {
    const interval = setInterval(() => {
    console.log("Checking map container:", mapContainer.value);
    if (mapContainer.value) {
        clearInterval(interval);
        initMap();
    }
    }, 200);
});
</script>