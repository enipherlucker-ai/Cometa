<script setup lang="ts">
import type { NuxtError } from '#app'
const props = defineProps<{ error: NuxtError }>()
</script>

<template>
 <main class="page">
   <img src="/cometa-logo.png" alt="" class="logo" width="160" height="160">
   <h1 v-if="props.error.statusCode === 404 ">Страница не найдена</h1>
   <h1 v-else>Что-то сломалось, пожалуйста подождите</h1>
   <button @click="clearError({ redirect: '/' })" > На главную </button>
 </main>
</template>

<style scoped>
.page {
  min-height: 100vh;
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 24px;
  text-align: center;
}

.logo {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  border: 3px solid var(--ink);
  padding: 8px;
  background: var(--surface);
  box-shadow: 10px 10px 0 var(--star);
}

h1 {
  max-width: 520px;
  font-size: clamp(24px, 4vw, 34px);
}
</style>
