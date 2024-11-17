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

      <div class="flex gap-2">
        <Button @click="handleFetchTripOptions" class="w-40">Get Trip Options</Button>
      </div>

      <Form v-if="tripOptions" :tripOptions="tripOptions"/>
      <p v-else>Enter a sentence describing your trip and the model you want to use</p>

      <ClearButton :visible="fieldsNotFilled" :onClear="clearInputAndResult"></ClearButton>
    </div>
  </div>
</template>


<script setup lang="ts">
import { useTrip } from '#build/imports';
import ModelSelector from '~/components/ModelSelector.vue';
import { toast } from '@/components/ui/toast/use-toast';

const { fetchTripOptions, tripOptions, errorMessage } = useTrip();
const sentence = ref('');
const selectedModel = ref('');

const fieldsNotFilled = computed(() => !!(sentence.value || selectedModel.value || tripOptions.value));

const handleFetchTripOptions = () => {
  if (!fieldsNotFilled) {
    errorMessage.value = 'Please provide a sentence and select a model.';
    toast({
      title: 'Uh oh! Something went wrong.',
      description: errorMessage.value,
      variant: 'destructive',
    })
    return;
  }
  fetchTripOptions(sentence.value, selectedModel.value);
}

const clearInputAndResult = () => {
  sentence.value = '';
  selectedModel.value = '';
  errorMessage.value = '';
  tripOptions.value = null;
}
</script>