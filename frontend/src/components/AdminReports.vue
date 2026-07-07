<template>
  <div>
    <h5 class="fw-bold mb-4">Library Reports</h5>
    
    <div v-if="reportData" class="row">
      <div class="col-md-4 mb-4">
        <div class="glass-card p-4 text-center h-100 d-flex flex-column justify-content-center">
          <h6 class="text-muted">Total Fines Collected</h6>
          <h2 class="fw-bold text-primary mb-0">${{ reportData.total_fines_collected.toFixed(2) }}</h2>
        </div>
      </div>
      
      <div class="col-md-8 mb-4">
        <div class="glass-card p-4 h-100">
          <h6 class="text-muted mb-3">Popular Titles</h6>
          <div v-for="pt in reportData.popular_titles" :key="pt.title" class="mb-2 d-flex justify-content-between align-items-center border-bottom pb-2">
            <span class="fw-bold">{{ pt.title }}</span>
            <span class="badge bg-primary rounded-pill">{{ pt.borrows }} borrows</span>
          </div>
          <div v-if="!reportData.popular_titles.length" class="text-muted small">No data yet</div>
        </div>
      </div>
      
      <div class="col-12">
        <div class="glass-card p-4">
          <h6 class="text-muted mb-3">Overdue Books</h6>
          <table class="table" v-if="reportData.overdue_list.length > 0">
            <thead><tr><th>Record ID</th><th>Book</th><th>User</th><th>Fine</th></tr></thead>
            <tbody>
              <tr v-for="o in reportData.overdue_list" :key="o.id">
                <td>#{{ o.id }}</td>
                <td class="fw-bold">{{ o.book_title }}</td>
                <td>{{ o.user_name }}</td>
                <td class="text-danger fw-bold">${{ o.fine_amount }}</td>
              </tr>
            </tbody>
          </table>
          <p v-else class="text-success fw-bold">No overdue books right now!</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/client'

const reportData = ref(null)

const fetchReport = async () => {
  try {
    const res = await api.get('/api/reports')
    reportData.value = res.data.data
  } catch (err) { console.error(err) }
}

onMounted(fetchReport)
</script>