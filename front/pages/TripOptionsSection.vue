<template>
    <div>
        <BackButton></BackButton>

        <h2 class="mt-10 scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight transition-colors first:mt-0">
            Trip options
        </h2>

        <div class="flex flex-col space-y-4 mt-5">
          <div class="flex gap-2">
            <Input
                class="w-1/2"
                type="text"
                v-model="sentence"
                placeholder="Enter a sentence describing your trip"
            />
            <Button @click="startVoiceRecognition" class="w-40">
                    <span v-if="!isListening">Use voice</span>
                    <span v-else>Listening ...</span>
            </Button>
          </div>

          <ModelSelector v-model="selectedModel" />

            
          <Button @click="handleFetchTripOptions" class="w-40">
            Get Trip Options
          </Button>
            

          <Form v-if="tripOptions" :tripOptions="tripOptions" />
          <p v-else>
              Enter a sentence describing your trip and the model you want to
              use
          </p>

          <ClearButton
              :visible="fieldsNotFilled"
              :onClear="clearInputAndResult">
          </ClearButton>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useTrip } from "#build/imports";
import ModelSelector from "~/components/ModelSelector.vue";
import { toast } from "@/components/ui/toast/use-toast";

const { fetchTripOptions, tripOptions, errorMessage } = useTrip();
const sentence = ref("");
const selectedModel = ref("");
const isListening = ref(false);

// TODO: export speechRecognition into another file
// Speech recognition setup
const recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let speechRecognition: SpeechRecognition | null = null;

if (recognition) {
  speechRecognition = new recognition();
  speechRecognition.lang = "fr-FR";
  speechRecognition.continuous = false;
  speechRecognition.interimResults = false;

  speechRecognition.onresult = (event) => {
    const result = event.results[0][0].transcript;
    sentence.value = result;
    isListening.value = false;
    
    toast({
      title: "Voice recognized",
      description: result,
      duration: 2000,
    });
  };

  speechRecognition.onerror = (event) => {
    console.error('Speech recognition error:', event.error);
    isListening.value = false;
    toast({
      title: "Voice Recognition Error",
      description: "Please try again",
      variant: "destructive",
    });
  };

  speechRecognition.onend = () => {
    isListening.value = false;
  };
};

const startVoiceRecognition = () => {
  if (!recognition) {
    toast({
      title: "Not Supported",
      description: "Speech recognition is not supported in your browser",
      variant: "destructive",
    });
    return;
  }

  if (isListening.value) {
    speechRecognition?.stop();
    isListening.value = false;
  } else {
    try {
      speechRecognition?.start();
      isListening.value = true;
    } catch (error) {
      console.error('Speech recognition error:', error);
      toast({
        title: "Error",
        description: "Failed to start voice recognition",
        variant: "destructive",
      });
    }
  }
};

const fieldsNotFilled = computed(
    () => !!(sentence.value || selectedModel.value || tripOptions.value),
);

const handleFetchTripOptions = () => {
    console.log(tripOptions.value);
    if (isEmpty(sentence.value)) {
        errorMessage.value = "Please provide a sentence.";
        toast({
            title: "Uh oh! Something went wrong.",
            description: errorMessage.value,
            variant: "destructive",
        });
        return;
    } else if (isEmpty(selectedModel.value)) {
        errorMessage.value = "Please provide a model.";
        toast({
            title: "Uh oh! Something went wrong.",
            description: errorMessage.value,
            variant: "destructive",
        });
        return;
    } else {
        fetchTripOptions(sentence.value, selectedModel.value);
    }
};

const clearInputAndResult = () => {
    sentence.value = "";
    selectedModel.value = "";
    errorMessage.value = "";
    tripOptions.value = null;
};

function isEmpty(str: string) {
    return !str || str.length === 0;
}
</script>
