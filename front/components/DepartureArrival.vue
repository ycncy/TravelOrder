<template>
    <div>
        <Popover v-model:open="open">
            <PopoverTrigger as-child>
                <Button
                    variant="outline"
                    size="sm"
                    class="w-[150px] justify-start"
                >
                    <template v-if="selectedCity">
                        {{ selectedCity?.label }}
                    </template>
                    <template v-else> + </template>
                </Button>
            </PopoverTrigger>
            <PopoverContent class="p-0" side="right" align="start">
                <Command>
                    <CommandList>
                        <CommandEmpty>No results found.</CommandEmpty>
                        <CommandGroup>
                            <CommandItem
                                v-for="option in options"
                                :key="option"
                                :value="option"
                                @select="() => selectOption(option)"
                            >
                                {{ option }}
                            </CommandItem>
                        </CommandGroup>
                    </CommandList>
                </Command>
            </PopoverContent>
        </Popover>
    </div>
</template>

<script setup lang="ts">
const open = ref(false);
const selectedCity = ref<Status>();

interface Status {
  value: string
  label: string
}

const props = defineProps({
  options: {
    type: Array as PropType<string[]>,
    default: () => [],
  },
});

const emit = defineEmits(['update:selected']);

function selectOption(option: string) {
  selectedCity.value = { value: option, label: option };
  emit('update:selected', option);
  open.value = false;
}
</script>