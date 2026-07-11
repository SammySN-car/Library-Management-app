<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const books = ref([])
const searchQuery = ref('')
const message = ref('')
const isSuccess = ref(false)
const token = localStorage.getItem('token')

const fetchBooks = async () => {
    try {
        const response = await axios.get('http://localhost:5000/books', {
            headers: { Authorization: `Bearer ${token}` }
        })
        books.value = response.data.all_books
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to fetch catalog'
        isSuccess.value = false
    }
}

const borrowBook = async (bookId) => {
    try {
        const response = await axios.post('http://localhost:5000/borrow', { book_id: bookId }, {
            headers: { Authorization: `Bearer ${token}` }
        })
        message.value = response.data.message || 'Book borrowed successfully'
        isSuccess.value = true
        fetchBooks()
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to borrow book'
        isSuccess.value = false
    }
}

const filteredBooks = computed(() => {
    if (!searchQuery.value) return books.value
    const query = searchQuery.value.toLowerCase()
    return books.value.filter(b => 
        b.title.toLowerCase().includes(query) ||
        b.author.toLowerCase().includes(query) ||
        b.genre.toLowerCase().includes(query)
    )
})

onMounted(() => {
    fetchBooks()
})
</script>

<template>
    <div>
        <h3 class="mb-4">Search & Borrow Books</h3>

        <div v-if="message" class="alert mb-3" :class="isSuccess ? 'alert-success' : 'alert-danger'" role="alert">
            {{ message }}
        </div>

        <div class="row mb-4">
            <div class="col-md-6">
                <input type="text" class="form-control form-control-lg shadow-sm" v-model="searchQuery" placeholder="Search by title, author, or genre...">
            </div>
        </div>

        <div class="table-responsive">
            <table class="table table-striped table-hover align-middle">
                <thead class="table-dark">
                    <tr>
                        <th>ID</th>
                        <th>Title</th>
                        <th>Author</th>
                        <th>Genre</th>
                        <th>Available Copies</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="book in filteredBooks" :key="book.id">
                        <td>{{ book.id }}</td>
                        <td><strong>{{ book.title }}</strong></td>
                        <td>{{ book.author }}</td>
                        <td><span class="badge bg-secondary">{{ book.genre }}</span></td>
                        <td>
                            <span v-if="book.available_copies > 0" class="badge bg-success">{{ book.available_copies }} copies left</span>
                            <span v-else class="badge bg-danger">Out of stock</span>
                        </td>
                        <td>
                            <button v-if="book.available_copies > 0" class="btn btn-primary btn-sm" @click="borrowBook(book.id)">
                                Borrow
                            </button>
                            <button v-else class="btn btn-secondary btn-sm" disabled>
                                Borrow
                            </button>
                        </td>
                    </tr>
                    <tr v-if="filteredBooks.length === 0">
                        <td colspan="6" class="text-center text-muted py-4">No books match your search.</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
