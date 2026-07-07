<template>
  <div>
    <h5 class="fw-bold mb-3">Issue / Return Desk</h5>
    
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="glass-card p-3">
          <h6 class="fw-bold mb-3">Issue Book to User</h6>
          <form @click.prevent>
            <div class="mb-2">
              <label class="small text-muted">User ID</label>
              <input type="number" v-model="issueForm.user_id" class="form-control" required>
            </div>
            <div class="mb-2">
              <label class="small text-muted">Book ID</label>
              <input type="number" v-model="issueForm.book_id" class="form-control" required>
            </div>
            <button class="btn btn-premium w-100 mt-2" @click="issueBook">Issue Book</button>
          </form>
        </div>
      </div>
    </div>
    
    <h6 class="fw-bold mb-2">All Borrow Records</h6>
    <div class="table-responsive">
      <table class="table align-middle text-sm">
        <thead class="table-light">
          <tr>
            <th>ID</th>
            <th>Book</th>
            <th>User</th>
            <th>Issue Date</th>
            <th>Due Date</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in records" :key="r.id">
            <td>#{{ r.id }}</td>
            <td class="fw-bold">{{ r.book_title }}</td>
            <td>{{ r.user_name }}</td>
            <td>{{ new Date(r.issue_date).toLocaleDateString() }}</td>
            <td><span class="text-danger">{{ new Date(r.due_date).toLocaleDateString() }}</span></td>
            <td>
              <span class="badge" :class="r.status === 'returned' ? 'bg-success' : 'bg-warning text-dark'">
                {{ r.status.toUpperCase() }}
              </span>
            </td>
            <td>
              <button v-if="r.status !== 'returned'" class="btn btn-sm btn-outline-success" @click="returnBook(r.id)">
                Mark Returned
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/client'

const records = ref([])
const issueForm = ref({ user_id: '', book_id: '' })

const fetchRecords = async () => {
  try {
    const res = await api.get('/api/borrow')
    records.value = res.data.data
  } catch (err) { console.error(err) }
}

const issueBook = async () => {
  if (!issueForm.value.user_id || !issueForm.value.book_id) return
  try {
    await api.post('/api/borrow', issueForm.value)
    issueForm.value = { user_id: '', book_id: '' }
    fetchRecords()
  } catch (err) {
    alert(err.response?.data?.message || 'Error issuing book')
  }
}

const returnBook = async (id) => {
  try {
    await api.put(`/api/borrow/${id}`)
    fetchRecords()
  } catch (err) {
    alert('Error returning book')
  }
}

onMounted(fetchRecords)
</script>