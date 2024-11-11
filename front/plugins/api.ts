import { defineNuxtPlugin } from '#app'
import { apiService } from '~/services/api'

export default defineNuxtPlugin(() => {
  return {
    provide: {
      apiService
    }
  }
})