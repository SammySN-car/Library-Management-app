<template>
  <div>
    <div class="mb-4">
      <input type="text" v-model="searchQuery" class="form-control form-control-premium p-3" placeholder="Search by title, author, or genre...">
    </div>
    
    <div class="row">
      <div v-for="book in filteredBooks" :key="book.id" class="col-md-4 mb-3">
        <div class="glass-card p-3 h-100 d-flex flex-column">
          <h5 class="fw-bold mb-1">{{ book.title }}</h5>
          <p class="text-secondary small mb-2">by {{ book.author }}</p>
          <span class="badge bg-light text-dark align-self-start mb-3">{{ book.genre }}</span>
          
          <div class="mt-auto d-flex justify-content-between align-items-center pt-3 border-top">
            <span class="small fw-bold" :class="book.available_copies > 0 ? 'text-success' : 'text-danger'">
              {{ book.available_copies > 0 ? 'Available' : 'Out of stock' }}
            </span>
            <button class="btn btn-sm btn-premium" :disabled="book.available_copies <= 0" @click="requestBorrow(book.id)">
              Borrow
            </button>
          </div>
        </div>
      </div>
      <div v-if="filteredBooks.length === 0" class="col-12 text-center text-muted py-5">
        No books found.
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api/client'

const books = ref([])
const searchQuery = ref('')

const filteredBooks = computed(() => {
  if (!searchQuery.value) return books.value
  const q = searchQuery.value.toLowerCase()
  return books.value.filter(b => 
    b.title.toLowerCase().includes(q) || 
    b.author.toLowerCase().includes(q) || 
    b.genre?.toLowerCase().includes(q)
  )
})

const fetchBooks = async () => {
  try {
    const res = await api.get('/api/books')
    books.value = res.data.data
  } catch(err) {}
}

const requestBorrow = async (book_id) => {
  try {
    await api.post('/api/borrow', { book_id })
    alert('Book borrowed successfully!')
    fetchBooks()
  } catch (err) {
    alert(err.response?.data?.message || 'Error borrowing book')
  }
}

onMounted(fetchBooks)
</script>