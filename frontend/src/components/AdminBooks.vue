<template>
  <div>
    <div class="d-flex justify-content-between mb-3">
      <h5 class="fw-bold">Manage Books</h5>
      <button class="btn btn-primary btn-sm" @click="showAddModal = true">+ Add Book</button>
    </div>
    
    <div class="table-responsive">
      <table class="table table-hover align-middle">
        <thead class="table-light">
          <tr>
            <th>Title</th>
            <th>Author</th>
            <th>ISBN</th>
            <th>Genre</th>
            <th>Available/Total</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in books" :key="book.id">
            <td class="fw-bold">{{ book.title }}</td>
            <td>{{ book.author }}</td>
            <td><small class="text-muted">{{ book.isbn }}</small></td>
            <td><span class="badge bg-secondary">{{ book.genre }}</span></td>
            <td>
              <span :class="book.available_copies > 0 ? 'text-success fw-bold' : 'text-danger fw-bold'">
                {{ book.available_copies }}
              </span> / {{ book.total_copies }}
            </td>
            <td>
              <button class="btn btn-sm btn-outline-primary me-2" @click="editBook(book)">Edit</button>
              <button class="btn btn-sm btn-outline-danger" @click="deleteBook(book.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Simple Add/Edit Modal using v-if instead of bootstrap js to avoid external deps -->
    <div v-if="showAddModal" class="position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center" style="background: rgba(0,0,0,0.5); z-index: 1050">
      <div class="glass-card p-4 bg-white" style="width: 500px; max-width: 90%">
        <h5 class="fw-bold mb-3">{{ editingId ? 'Edit Book' : 'Add New Book' }}</h5>
        <form @submit.prevent="saveBook">
          <div class="mb-2">
            <label class="small fw-bold">Title</label>
            <input type="text" v-model="form.title" class="form-control" required>
          </div>
          <div class="mb-2">
            <label class="small fw-bold">Author</label>
            <input type="text" v-model="form.author" class="form-control" required>
          </div>
          <div class="mb-2">
            <label class="small fw-bold">ISBN</label>
            <input type="text" v-model="form.isbn" class="form-control" required>
          </div>
          <div class="row mb-3">
            <div class="col-6">
              <label class="small fw-bold">Genre</label>
              <input type="text" v-model="form.genre" class="form-control">
            </div>
            <div class="col-6">
              <label class="small fw-bold">Total Copies</label>
              <input type="number" v-model="form.total_copies" class="form-control" min="1" required>
            </div>
          </div>
          <div class="d-flex justify-content-end gap-2">
            <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
            <button type="submit" class="btn btn-premium">Save Book</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/client'

const books = ref([])
const showAddModal = ref(false)
const editingId = ref(null)
const form = ref({ title: '', author: '', isbn: '', genre: '', total_copies: 1 })

const fetchBooks = async () => {
  try {
    const res = await api.get('/api/books')
    books.value = res.data.data
  } catch (err) {
    console.error(err)
  }
}

const editBook = (book) => {
  editingId.value = book.id
  form.value = { ...book }
  showAddModal.value = true
}

const deleteBook = async (id) => {
  if (confirm('Are you sure you want to delete this book?')) {
    await api.delete(`/api/books/${id}`)
    fetchBooks()
  }
}

const saveBook = async () => {
  try {
    if (editingId.value) {
      await api.put(`/api/books/${editingId.value}`, form.value)
    } else {
      await api.post('/api/books', form.value)
    }
    closeModal()
    fetchBooks()
  } catch (err) {
    alert(err.response?.data?.message || 'Error saving book')
  }
}

const closeModal = () => {
  showAddModal.value = false
  editingId.value = null
  form.value = { title: '', author: '', isbn: '', genre: '', total_copies: 1 }
}

onMounted(() => {
  fetchBooks()
})
</script>
