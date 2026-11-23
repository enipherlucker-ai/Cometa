<script setup lang="ts">
import type { User } from '~/types/user'

useHead({title: 'Авторизация'})

const currentUser = useCurrentUser()
const login = ref('')
const password = ref('')
const errorText = ref('')
const loading = ref(false)

async function onSubmit() {
  errorText.value = ''
  loading.value = true
  try {
    currentUser.value = await $fetch<User>('/api/auth/login', {
      method: 'POST',
      body: {login: login.value, password: password.value},
    })
    await navigateTo('/')
  } catch (error) {
    const status = (error as {statusCode?: number}).statusCode
    if (status === 401) {
      errorText.value = 'Неверный логин или пароль'
    } else if (status === 422) {
      errorText.value = 'Логин или пароль не подходят по формату'
    } else if (status === 502 || status === 503) {
      errorText.value = 'Технические работы, сервис авторизации недоступен, пожалуйста подождите'
    } else {
      errorText.value = 'Сервер не отвечает'
    }
  } finally {
    loading.value = false
  }

}
</script>

<template>
  <main class="page">
    <form class="card" @submit.prevent="onSubmit">
      <div class="brand">
        <img src="/cometa-logo.png" alt="" class="brand-logo" width="56" height="56">
        <span class="brand-name">Cometa</span>
      </div>

      <h1>Вход</h1>
      <p v-if="errorText" class="error">{{ errorText }}</p>

      <label>
        Логин
        <input v-model="login" autocomplete="username" required>
      </label>

      <label>
        Пароль
        <input v-model="password" type="password" autocomplete="current-password" required>
      </label>

      <button type="submit" :disabled="loading">{{ loading ? 'Входим' : 'Войти' }}</button>
    </form>
  </main>
</template>

<style scoped>
.page {
  min-height: 100vh;
  padding: 24px 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card {
  width: 100%;
  max-width: 360px;
  padding: 32px 28px;
  background: var(--surface);
  border: 2px solid var(--ink);
  border-radius: var(--radius-m);
  box-shadow: 8px 8px 0 var(--star);
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-logo {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: 2px solid var(--ink);
  padding: 3px;
  background: var(--surface);
}

.brand-name {
  font-family: var(--font-display);
  font-weight: 500;
  font-size: 18px;
}

h1 {
  font-size: 28px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 14px;
  font-weight: 500;
}

button {
  margin-top: 4px;
}

.error {
  margin: 0;
  padding: 10px 14px;
  border-radius: var(--radius-s);
  background: var(--danger-bg);
  color: var(--danger);
  font-size: 14px;
}
</style>
