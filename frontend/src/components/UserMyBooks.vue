<template>
  <div>
    <div class="row">
      <div v-for="r in myBooks" :key="r.id" class="col-md-6 mb-3">
        <div class="glass-card p-3 position-relative">
          <div class="position-absolute top-0 end-0 m-3">
             <span class="badge" :class="r.status === 'returned' ? 'bg-success' : (r.status === 'overdue' ? 'bg-danger' : 'bg-primary')">
               {{ r.status.toUpperCase() }}
             </span>
          </div>
          <h5 class="fw-bold pe-5">{{ r.book_title }}</h5>
          <p class="text-muted small mb-3">Issued: {{ new Date(r.issue_date).toLocaleDateString() }}</p>
          
          <div class="d-flex justify-content-between align-items-end mt-2 pt-2 border-top">
            <div>
              <p class="mb-0 small fw-bold text-secondary">Due Date</p>
              <p class="mb-0 fw-bold" :class="new Date(r.due_date) < new Date() && r.status !== 'returned' ? 'text-danger' : ''">
                {{ new Date(r.due_date).toLocaleDateString() }}
              </p>
            </div>
            <button v-if="r.status !== 'returned'" class="btn btn-outline-primary btn-sm px-4" @click="returnBook(r.id)">
              Return
            </button>
          </div>
        </div>
      </div>
      <div v-if="myBooks.length === 0" class="col-12 text-center text-muted py-5">
        You haven't borrowed any books yet.
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/client'

const myBooks = ref([])

const fetchMyBooks = async () => {
  try {
    const res = await api.get('/api/my-books')
    myBooks.value = res.data.data
  } catch(err) {}
}

const returnBook = async (id) => {
  try {
    await api.put(`/api/borrow/${id}`)
    fetchMyBooks()
  } catch (err) {
    alert('Error returning book')
  }
}

onMounted(fetchMyBooks)
</script>