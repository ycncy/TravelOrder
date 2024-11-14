<template>
  <h3 class="mt-8 scroll-m-20 text-2xl font-semibold tracking-tight">Total travel time: {{ trip.total_time }}</h3>

  <Table>
    <TableCaption>Steps</TableCaption>
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
        <TableCell>{{ step.travel_time }}</TableCell>
        <TableCell>{{ step.departure_station }}</TableCell>
        <TableCell>{{ step.departure_city }}</TableCell>
        <TableCell>{{ step.arrival_station }}</TableCell>
        <TableCell>{{ step.arrival_city }}</TableCell>
      </TableRow>
    </TableBody>
  </Table>

</template>

<script setup lang="ts">
import type { TripResponse } from "~/types";

defineProps<{
  trip: TripResponse;
}>();
</script>
