<script setup lang="ts">
import BackButton from "~/components/BackButton.vue";
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
</script>

<template>
<div class="w-full">
  <BackButton></BackButton>

  <h2
      class="mt-10 scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight transition-colors first:mt-0"
  >
    Train dataset map
  </h2>

  <Tabs default-value="ter" class="w-full mt-2">
    <TabsList class="w-full">
      <TabsTrigger value="ter" class="w-full">
        TER
      </TabsTrigger>
      <TabsTrigger value="tgv" class="w-full">
        TGV
      </TabsTrigger>
      <TabsTrigger value="intercites" class="w-full">
        Intercites
      </TabsTrigger>
    </TabsList>
    <TabsContent value="ter">
      <div>
        <iframe src="/static/maps/ter.html"
                frameborder="0" style="width: 100%; height: 100vh; border-radius: 5px"></iframe>
      </div>
    </TabsContent>
    <TabsContent value="tgv">
      <div>
        <iframe src="/static/maps/tgv.html"
                frameborder="0" style="width: 100%; height: 100vh; border-radius: 5px"></iframe>
      </div>
    </TabsContent>
    <TabsContent value="intercites">
      <div>
        <iframe src="/static/maps/intercites.html"
                frameborder="0" style="width: 100%; height: 100vh; border-radius: 5px"></iframe>
      </div>
    </TabsContent>
  </Tabs>
</div>
</template>

<style scoped>

</style>