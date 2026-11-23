<script setup lang="ts">
import type {ReceiptRow} from '~/types/receipt'

const requestFetch = useRequestFetch()

useHead({title: 'Чеки'})

const rows = ref<ReceiptRow[]>([])
const loadError = ref('')

const formOpen = ref(false)
const rawReceipt = ref('')
const submitError = ref('')
const submitting = ref(false)

async function loadReceipts() {
  loadError.value = ''

  try {
    rows.value = await requestFetch<ReceiptRow[]>(
        '/api/receipt/get_compound',
        {
          query: {
            limit: 50,
            offset: 0,
          }
        },
    )
  } catch {
    loadError.value = 'Не удалось загрузить чеки'
  }


}

function openForm() {
  rawReceipt.value = ''
  submitError.value = ''
  formOpen.value = true
}

function closeForm() {
  formOpen.value = false
}

async function onSubmit() {
  submitError.value = ''
  submitting.value = true
  try {
    await $fetch('/api/create_receipt', {method: 'POST', body: {raw_receipt: rawReceipt.value}})
    closeForm()
    await loadReceipts()
  } catch (error) {
    submitError.value = 'Не удалось добавить чек'
  } finally {
    submitting.value = false
  }
}

await loadReceipts()
</script>

<template>
  <main class="page">
    <header class="topbar">
      <NuxtLink to="/" class="home-link" aria-label="На главную">
        <img src="/cometa-logo.png" alt="" width="44" height="44">
      </NuxtLink>
      <h1>Чеки</h1>
      <div class="topbar-actions">
        <NuxtLink to="/" class="back-link">На главную</NuxtLink>
        <button @click="openForm">Добавить чек</button>
      </div>
    </header>

    <p v-if="loadError" class="error">{{ loadError }}</p>

    <section v-if="rows.length === 0" class="empty">
      <img src="/cometa-logo.png" alt="" width="120" height="120">
      <p>
        У вас ничего. Хотите <a href="#" @click.prevent="openForm">добавить чек</a>?
      </p>
    </section>

    <div v-else class="table-wrap">
      <table>
        <thead>
        <tr>
          <th>Дата время</th>
          <th>Товар</th>
          <th class="num">Чек</th>
          <th>Категория</th>
          <th class="num">НДС</th>
          <th class="num">Сумма НДС</th>
          <th class="num">Цена</th>
          <th class="num">Кол-во</th>
          <th class="num">Итог</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="row in rows" :key="row.id">
          <td class="date">{{ row.period }}</td>
          <td class="name">{{ row.name }}</td>
          <td class="num muted">{{ row.receipt_id }}</td>
          <td><span class="tag">{{ row.group_name }}</span></td>
          <td class="num muted">{{ row.vat }}</td>
          <td class="num muted">{{ row.vat_sum }}</td>
          <td class="num">{{ row.price }}</td>
          <td class="num">{{ row.quantity }}</td>
          <td class="num total">{{ row.sum }}</td>
        </tr>
        </tbody>
      </table>
    </div>

    <div v-if="formOpen" class="overlay" @click.self="closeForm">
      <form class="card" @submit.prevent="onSubmit">
        <h2>Добавить чек</h2>
        <p v-if="submitError" class="error">{{ submitError }}</p>

        <label>
          Строка чека
          <input v-model="rawReceipt" placeholder="t=20261010T2119&s=5099.62&fn=...&i=...&fp=...&n=1" required>
        </label>

        <div class="actions">
          <button type="button" class="secondary" @click="closeForm">Отмена</button>
          <button type="submit" :disabled="submitting">{{ submitting ? 'Отправляем' : 'Отправить' }}</button>
        </div>
      </form>
    </div>
  </main>
</template>

<style scoped>
.page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.topbar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.home-link img {
  display: block;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 2px solid var(--ink);
  padding: 2px;
  background: var(--surface);
}

h1 {
  font-size: 30px;
}

.topbar-actions {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 20px;
}

.back-link {
  color: var(--ink-soft);
  font-weight: 500;
}

.table-wrap {
  overflow-x: auto;
  background: var(--surface);
  border: 1.5px solid var(--line);
  border-radius: var(--radius-m);
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

th,
td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid var(--line);
  white-space: nowrap;
}

th {
  font-weight: 600;
  color: var(--ink-soft);
  background: #f6f7fb;
}

tbody tr:last-child td {
  border-bottom: none;
}

tbody tr:hover {
  background: #f6f7fb;
}

.num {
  text-align: right;
  font-variant-numeric: tabular-nums;
}

.muted,
.date {
  color: var(--ink-soft);
}

.name {
  white-space: normal;
  min-width: 200px;
  font-weight: 500;
}

.total {
  font-weight: 600;
}

.tag {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 999px;
  background: #e7eafb;
  color: var(--accent-hover);
  font-size: 13px;
}

.empty {
  padding: 56px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  text-align: center;
  background: var(--surface);
  border: 1.5px dashed var(--line);
  border-radius: var(--radius-m);
  color: var(--ink-soft);
}

.empty img {
  border-radius: 50%;
  opacity: 0.85;
}

.empty p {
  margin: 0;
  font-size: 17px;
}

.overlay {
  position: fixed;
  inset: 0;
  padding: 16px;
  background: rgba(26, 33, 66, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
}

.card {
  width: 100%;
  max-width: 460px;
  padding: 28px;
  background: var(--surface);
  border: 2px solid var(--ink);
  border-radius: var(--radius-m);
  box-shadow: 8px 8px 0 var(--star);
  display: flex;
  flex-direction: column;
  gap: 18px;
}

h2 {
  font-size: 22px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 14px;
  font-weight: 500;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

button.secondary {
  background: transparent;
  border-color: var(--line);
  color: var(--ink);
}

button.secondary:hover:not(:disabled) {
  background: #f6f7fb;
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

.card .error {
  margin: 0;
}

@media (max-width: 640px) {
  .page {
    padding: 16px;
  }

  .topbar {
    flex-wrap: wrap;
  }

  .topbar-actions {
    width: 100%;
    margin-left: 0;
    justify-content: space-between;
  }
}
</style>
