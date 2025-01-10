<template>
  <h3 class="mt-8 scroll-m-20 text-2xl font-semibold tracking-tight">Total travel time: {{ formatTime(trip.total_time) }}</h3>

  <div class="flex gap-4 mt-4">
    <ScrollArea class="h-[500px] w-[50%] rounded-lg border p-4">
      <Table>
        <TableCaption>Trip Steps</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead>Travel time</TableHead>
            <TableHead>Departure station</TableHead>
            <TableHead>Departure city</TableHead>
            <TableHead>Arrival station</TableHead>
            <TableHead>Arrival city</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow v-for="(step, index) in trip.steps" :key="index">
            <TableCell class="w-32">{{ formatTime(step.travel_time) }}</TableCell>
            <TableCell>{{ step.departure_station }}</TableCell>
            <TableCell>{{ step.departure_city }}</TableCell>
            <TableCell>{{ step.arrival_station }}</TableCell>
            <TableCell>{{ step.arrival_city }}</TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </ScrollArea>

    <div class="w-[50%] h-[500px] rounded-lg border overflow-hidden">
      <TripMap v-show="trip.steps.length > 0" :steps="trip.steps" />
    </div>
  </div>
  
</template>

<script setup lang="ts">
import type { TripResponse } from "~/types";
import { minutesToHours } from "~/utils/timeUtils";
import TripMap from "~/components/TripMap.vue"; 

defineProps<{
  trip: TripResponse;
}>();

const formatTime = (minutes: number) => minutesToHours(minutes);
</script>
