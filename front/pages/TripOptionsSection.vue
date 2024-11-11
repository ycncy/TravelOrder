<template>
  <div>
    <BackButton></BackButton>

    <h2
      class="mt-10 scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight transition-colors first:mt-0"
    >
      Trip options
    </h2>

    <div class="flex flex-col space-y-4 mt-5">
      <Input
        class="w-1/2"
        type="text"
        v-model="sentence"
        placeholder="Enter a sentence describing your trip"
      />
      <ModelSelector v-model="selectedModel" />
      <Button @click="handleFetchTripOptions" class="w-40"
        >Get Trip Options</Button
      >

      <div v-if="tripOptions">
        <h3>Result:</h3>
        <pre>{{ tripOptions }}</pre>
      </div>
      <p v-else-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>
      <p v-else>Enter a sentence describing your trip and the model you want to use</p>
    </div>
  </div>
</template>


<script setup lang="ts">
import { useTrip } from '#build/imports';
import ModelSelector from '~/components/ModelSelector.vue'

const { fetchTripOptions, tripOptions, errorMessage } = useTrip();
const sentence = ref('');
const selectedModel = ref('');

const handleFetchTripOptions = () => {
  if (!sentence.value || !selectedModel.value) {
    errorMessage.value = 'Please provide a sentence and select a model.';
    return;
  }
  fetchTripOptions(sentence.value, selectedModel.value);
}
</script>