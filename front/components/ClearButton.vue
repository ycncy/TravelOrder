<template>
    <Button
        v-if="visible"
        @click="onClear"
        class="w-20"
        :variant="variant"
    >
        Clear
    </Button>
</template>


<script setup lang="ts">
import type { PropType } from 'vue';
import type { ButtonVariants } from './ui/button';

defineProps({
    visible: {
        type: Boolean, 
        required: true
    }, 

    onClear: {
        type: Function as PropType<() => void>,
        required: true,
    },

    variant: {
        type: String as PropType<ButtonVariants["variant"]>,
        default: 'outline',
    },
});

</script>