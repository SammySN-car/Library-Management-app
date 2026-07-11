<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const books = ref([])
const message = ref('')
const isSuccess = ref(false)
const token = localStorage.getItem('token')

// Form states
const showAddForm = ref(false)
const showEditForm = ref(false)

const newBook = ref({
    title: '',
    author: '',
    isbn: '',
    genre: '',
    total_copies: 1,
    price: 0
})

const editBookData = ref({
    id: null,
    title: '',
    author: '',
    isbn: '',
    genre: '',
    total_copies: 1,
    price: 0
})

const fetchBooks = async () => {
    try {
        const response = await axios.get('http://localhost:5000/books', {
            headers: { Authorization: `Bearer ${token}` }
        })
        books.value = response.data.all_books
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to fetch books'
        isSuccess.value = false
    }
}

const addBook = async () => {
    try {
        const response = await axios.post('http://localhost:5000/admin/book', newBook.value, {
            headers: { Authorization: `Bearer ${token}` }
        })
        message.value = response.data.message || 'Book added successfully'
        isSuccess.value = true
        showAddForm.value = false
        // Reset form
        newBook.value = { title: '', author: '', isbn: '', genre: '', total_copies: 1, price: 0 }
        fetchBooks()
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to add book'
        isSuccess.value = false
    }
}

const editBook = (book) => {
    editBookData.value = { ...book }
    showEditForm.value = true
    showAddForm.value = false
}

const updateBook = async () => {
    try {
        const response = await axios.put(`http://localhost:5000/admin/book/${editBookData.value.id}`, editBookData.value, {
            headers: { Authorization: `Bearer ${token}` }
        })
        message.value = response.data.message || 'Book updated successfully'
        isSuccess.value = true
        showEditForm.value = false
        fetchBooks()
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to update book'
        isSuccess.value = false
    }
}

const deleteBook = async (bookId) => {
    if (!confirm('Are you sure you want to delete this book?')) return
    try {
        const response = await axios.delete(`http://localhost:5000/admin/book/${bookId}`, {
            headers: { Authorization: `Bearer ${token}` }
        })
        message.value = response.data.message || 'Book deleted successfully'
        isSuccess.value = true
        fetchBooks()
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to delete book'
        isSuccess.value = false
    }
}

onMounted(() => {
    fetchBooks()
})
</script>

<template>
    <div>
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h3>Manage Books Catalog</h3>
            <button class="btn btn-success" @click="showAddForm = !showAddForm; showEditForm = false">
                {{ showAddForm ? 'Cancel' : 'Add New Book' }}
            </button>
        </div>

        <div v-if="message" class="alert mb-3" :class="isSuccess ? 'alert-success' : 'alert-danger'" role="alert">
            {{ message }}
        </div>

        <!-- Add Book Form -->
        <div v-if="showAddForm" class="card bg-light mb-4 shadow-sm border-0">
            <div class="card-body">
                <h5 class="card-title">Add New Book</h5>
                <form @submit.prevent="addBook">
                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label">Title</label>
                            <input type="text" class="form-control" v-model="newBook.title" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Author</label>
                            <input type="text" class="form-control" v-model="newBook.author" required>
                        </div>
                        <div class="col-md-4">
                            <label class="form-label">ISBN</label>
                            <input type="text" class="form-control" v-model="newBook.isbn" required>
                        </div>
                        <div class="col-md-4">
                            <label class="form-label">Genre</label>
                            <input type="text" class="form-control" v-model="newBook.genre" required placeholder="e.g., Fiction, Tech">
                        </div>
                        <div class="col-md-2">
                            <label class="form-label">Total Copies</label>
                            <input type="number" class="form-control" v-model.number="newBook.total_copies" min="1" required>
                        </div>
                        <div class="col-md-2">
                            <label class="form-label">Price ($)</label>
                            <input type="number" class="form-control" v-model.number="newBook.price" min="0">
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary mt-3">Submit Book</button>
                </form>
            </div>
        </div>

        <!-- Edit Book Form -->
        <div v-if="showEditForm" class="card bg-light mb-4 shadow-sm border-0 border-start border-primary border-4">
            <div class="card-body">
                <h5 class="card-title">Edit Book: {{ editBookData.title }}</h5>
                <form @submit.prevent="updateBook">
                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label">Title</label>
                            <input type="text" class="form-control" v-model="editBookData.title" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Author</label>
                            <input type="text" class="form-control" v-model="editBookData.author" required>
                        </div>
                        <div class="col-md-4">
                            <label class="form-label">ISBN</label>
                            <input type="text" class="form-control" v-model="editBookData.isbn" required>
                        </div>
                        <div class="col-md-4">
                            <label class="form-label">Genre</label>
                            <input type="text" class="form-control" v-model="editBookData.genre" required>
                        </div>
                        <div class="col-md-2">
                            <label class="form-label">Total Copies</label>
                            <input type="number" class="form-control" v-model.number="editBookData.total_copies" min="1" required>
                        </div>
                        <div class="col-md-2">
                            <label class="form-label">Price ($)</label>
                            <input type="number" class="form-control" v-model.number="editBookData.price" min="0">
                        </div>
                    </div>
                    <div class="mt-3">
                        <button type="submit" class="btn btn-primary me-2">Save Changes</button>
                        <button type="button" class="btn btn-secondary" @click="showEditForm = false">Cancel</button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Books Table -->
        <div class="table-responsive">
            <table class="table table-striped table-hover align-middle">
                <thead class="table-dark">
                    <tr>
                        <th>ID</th>
                        <th>Title</th>
                        <th>Author</th>
                        <th>ISBN</th>
                        <th>Genre</th>
                        <th>Copies (Avail/Total)</th>
                        <th>Price</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="book in books" :key="book.id">
                        <td>{{ book.id }}</td>
                        <td>{{ book.title }}</td>
                        <td>{{ book.author }}</td>
                        <td><code>{{ book.isbn }}</code></td>
                        <td><span class="badge bg-info text-dark">{{ book.genre }}</span></td>
                        <td>{{ book.available_copies }} / {{ book.total_copies }}</td>
                        <td>${{ book.price }}</td>
                        <td>
                            <button class="btn btn-sm btn-outline-primary me-2" @click="editBook(book)">Edit</button>
                            <button class="btn btn-sm btn-outline-danger" @click="deleteBook(book.id)">Delete</button>
                        </td>
                    </tr>
                    <tr v-if="books.length === 0">
                        <td colspan="8" class="text-center text-muted py-4">No books found in the catalog.</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
