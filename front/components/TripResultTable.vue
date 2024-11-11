<template>
  <Table>
    <TableCaption>Result</TableCaption>
    <TableHeader>
      <TableRow>
        <TableHead>Total time</TableHead>
        <TableHead>Departure station</TableHead>
        <TableHead>Departure city</TableHead>
        <TableHead>Arrival station</TableHead>
        <TableHead>Arrival city</TableHead>
      </TableRow>
    </TableHeader>
    <TableBody>
      <TableRow v-for="(step, index) in trip.steps" :key="index">
        <TableCell>{{ trip.total_time }}</TableCell>
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
