<template>
  <Button class="w-20" @click="navigateBack">Back</Button>
</template>

<script setup lang="ts">
const router = useRouter()

const navigateBack = () => {
  router.push('/');
}
</script>
