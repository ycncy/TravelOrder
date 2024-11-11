<template>
  <Popover v-model:open="open">
    <PopoverTrigger as-child>
      <Button
        variant="outline"
        role="combobox"
        :aria-expanded="open"
        class="w-[200px] justify-between"
      >
        {{ modelValue || "Select model..." }}
      </Button>
    </PopoverTrigger>
    <PopoverContent class="w-[200px] p-0">
      <Command>
        <CommandEmpty>No model found.</CommandEmpty>
        <CommandList>
          <CommandGroup>
            <CommandItem
              v-for="model in models"
              :key="model.value"
              :value="model.value"
              @select="handleSelect"
            >
              {{ model.label }}
            </CommandItem>
          </CommandGroup>
        </CommandList>
      </Command>
    </PopoverContent>
  </Popover>
</template>

<script setup lang="ts">
import { 
  Popover,
  PopoverContent,
  PopoverTrigger
} from '@/components/ui/popover'
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandItem,
  CommandList,
} from '@/components/ui/command'
import { Button } from '@/components/ui/button'

const props = defineProps<{
  modelValue: string;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
}>();

const open = ref(false);

const models = [
  { value: "SPACY", label: "SPACY" },
  { value: "CAMEMBERT", label: "CAMEMBERT" },
];

const handleSelect = (event: any) => {
  emit("update:modelValue", event.detail.value);
  open.value = false;
};
</script>
