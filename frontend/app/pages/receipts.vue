<script setup lang="ts">
import type { ReceiptRow } from '~/types/receipt'

useHead({title: 'Чеки'})

const rows = ref<ReceiptRow[]>([])
const loadError = ref('')

const formOpen = ref(false)
const rawReceipt = ref('')
const submitError = ref('')
const submitting = ref(false)

async function loadReceipts() {
  loadError.value = ''
  // TODO: загрузка строк чеков из API, например:
  // rows.value = await $fetch<ReceiptRow[]>('/api/receipts')
  rows.value = []
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
    // TODO: отправка строки чека в API, например:
    // await $fetch('/api/create_receipt', {method: 'POST', body: {raw_receipt: rawReceipt.value}})
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
    <section class="content">
      <h1>Чеки</h1>
      <p v-if="loadError" class="error">{{ loadError }}</p>

      <p v-if="rows.length === 0" class="empty">
        У вас ничего. Хотите <a href="#" @click.prevent="openForm">добавить чек</a>?
      </p>

      <table v-else>
        <thead>
          <tr>
            <th>Дата время</th>
            <th>Товар</th>
            <th>Чек</th>
            <th>Категория</th>
            <th>НДС</th>
            <th>Сумма НДС</th>
            <th>Цена</th>
            <th>Кол-во</th>
            <th>Итог</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows" :key="row.id">
            <td>{{ row.period }}</td>
            <td>{{ row.name }}</td>
            <td>{{ row.receipt_id }}</td>
            <td>{{ row.group_name }}</td>
            <td>{{ row.vat }}</td>
            <td>{{ row.vat_sum }}</td>
            <td>{{ row.price }}</td>
            <td>{{ row.quantity }}</td>
            <td>{{ row.sum }}</td>
          </tr>
        </tbody>
      </table>
    </section>

    <aside class="sidebar">
      <button @click="openForm">Добавить чек</button>
      <NuxtLink to="/">На главную</NuxtLink>
    </aside>

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
  display: flex;
  gap: 24px;
  padding: 24px;
  align-items: flex-start;
}

.content {
  flex: 1;
  overflow-x: auto;
}

.sidebar {
  width: 180px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

h1, h2 {
  margin: 0 0 16px;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

th, td {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  text-align: left;
  font-size: 14px;
}

th {
  background: #e5e7eb;
}

.empty {
  color: #6b7280;
}

.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
}

.card {
  width: 420px;
  padding: 24px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 14px;
}

input {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 16px;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

button {
  padding: 10px;
  border: none;
  border-radius: 8px;
  background: #2563eb;
  color: white;
  font-size: 16px;
  cursor: pointer;
}

button.secondary {
  background: #e5e7eb;
  color: #111827;
}

button:disabled {
  background: #93c5fd;
  cursor: wait;
}

.error {
  margin: 0;
  color: #dc2626;
  font-size: 14px;
}
</style>
