<script setup lang="ts">
const currentUser = useCurrentUser()
const logoutError = ref('')

useHead({title: 'Главная'})

async function onLogout(){
  logoutError.value = ''
  try {
    await $fetch('/api/auth/logout', {method: 'POST'})
    currentUser.value = null
    await navigateTo('/login')
  } catch (err) {
    logoutError.value = 'Сервис авторизации недоступен, пожалуйста подождите'
  }

}

</script>

<template>
  <main class="home">
    <div class="logo-frame">
      <img src="/cometa-logo.png" alt="Логотип Cometa" class="logo" width="256" height="256">
    </div>

    <section class="hello">
      <h1>Привет, {{ currentUser?.name }}!</h1>
      <p class="lead">Здесь хранятся ваши чеки: добавляйте новые и смотрите, на что уходят деньги.</p>
      <p v-if="logoutError" class="error">{{ logoutError }}</p>
      <div class="actions">
        <NuxtLink to="/receipts" class="primary-link">Мои чеки</NuxtLink>
        <button class="ghost" @click="onLogout">Выйти</button>
      </div>
    </section>
  </main>
</template>

<style scoped>
.home {
  min-height: 100vh;
  max-width: 960px;
  margin: 0 auto;
  padding: 48px 24px;
  display: flex;
  align-items: center;
  gap: 64px;
}

/* Рисунок в круге, за ним жёлтый «след кометы» со сдвигом */
.logo-frame {
  position: relative;
  flex: none;
  width: 280px;
  height: 280px;
}

.logo-frame::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: var(--star);
  transform: translate(14px, 14px);
}

.logo {
  position: relative;
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 3px solid var(--ink);
  background: var(--surface);
  object-fit: contain;
  padding: 12px;
}

.hello {
  max-width: 460px;
}

h1 {
  font-size: clamp(32px, 5vw, 48px);
}

.lead {
  margin: 16px 0 32px;
  font-size: 18px;
  color: var(--ink-soft);
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.primary-link {
  display: inline-block;
  padding: 11px 24px;
  border: 2px solid var(--accent);
  border-radius: var(--radius-s);
  background: var(--accent);
  color: #fff;
  font-weight: 600;
  text-decoration: none;
  transition: background-color 0.15s, border-color 0.15s;
}

.primary-link:hover {
  background: var(--accent-hover);
  border-color: var(--accent-hover);
  color: #fff;
}

button.ghost {
  background: transparent;
  border-color: var(--line);
  color: var(--ink);
}

button.ghost:hover:not(:disabled) {
  background: var(--surface);
  border-color: var(--ink-soft);
}

.error {
  margin: 0 0 16px;
  padding: 10px 14px;
  border-radius: var(--radius-s);
  background: var(--danger-bg);
  color: var(--danger);
  font-size: 14px;
}

@media (max-width: 720px) {
  .home {
    flex-direction: column;
    justify-content: center;
    gap: 40px;
    text-align: center;
  }

  .logo-frame {
    width: 200px;
    height: 200px;
  }

  .logo-frame::before {
    transform: translate(10px, 10px);
  }

  .actions {
    justify-content: center;
  }
}
</style>
