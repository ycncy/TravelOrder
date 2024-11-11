<template>
  <div>
    <h1 class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">
      [T-AIA-901] Travel Order Resolver
    </h1>

    <p class="leading-7 [&:not(:first-child)]:mt-6">
      This is a simple client for our project in which contains 2 API calls to showcase our model training process.
    </p>

    <div class="flex-row mt-6">
      <Button class="w-30 mr-3">
        <NuxtLink to="/ShortestTripSection">Shortest trip</NuxtLink>
      </Button>

      <Button>
        <NuxtLink class="w-30" to="/TripOptionsSection">Trip options</NuxtLink>
      </Button>
    </div>

    <NuxtPage/>
  </div>
</template>