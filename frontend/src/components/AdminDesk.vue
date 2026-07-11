<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const borrowRecords = ref([])
const message = ref('')
const isSuccess = ref(false)
const token = localStorage.getItem('token')

const newIssue = ref({
    book_id: '',
    user_id: ''
})

const fetchBorrows = async () => {
    try {
        const response = await axios.get('http://localhost:5000/borrows', {
            headers: { Authorization: `Bearer ${token}` }
        })
        borrowRecords.value = response.data.all_records
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to fetch borrow records'
        isSuccess.value = false
    }
}

const issueBook = async () => {
    try {
        const response = await axios.post('http://localhost:5000/admin/issue', newIssue.value, {
            headers: { Authorization: `Bearer ${token}` }
        })
        message.value = response.data.message || 'Book issued successfully'
        isSuccess.value = true
        // Reset form
        newIssue.value = { book_id: '', user_id: '' }
        fetchBorrows()
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to issue book'
        isSuccess.value = false
    }
}

const processReturn = async (recordId) => {
    try {
        const response = await axios.put(`http://localhost:5000/admin/return/${recordId}`, {}, {
            headers: { Authorization: `Bearer ${token}` }
        })
        const fine = response.data.fine_amount || 0
        message.value = `Book returned successfully. Fine amount: $${fine}`
        isSuccess.value = true
        fetchBorrows()
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to process return'
        isSuccess.value = false
    }
}

onMounted(() => {
    fetchBorrows()
})
</script>

<template>
    <div>
        <h3 class="mb-4">Issue & Return Desk</h3>

        <div v-if="message" class="alert mb-3" :class="isSuccess ? 'alert-success' : 'alert-danger'" role="alert">
            {{ message }}
        </div>

        <div class="row g-4">
            <!-- Issue Book Column -->
            <div class="col-md-4">
                <div class="card bg-light border-0 shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title mb-3">Issue Book</h5>
                        <form @submit.prevent="issueBook">
                            <div class="mb-3">
                                <label for="book_id" class="form-label">Book ID</label>
                                <input type="number" class="form-control" id="book_id" v-model.number="newIssue.book_id" required placeholder="Enter Book ID">
                            </div>
                            <div class="mb-3">
                                <label for="user_id" class="form-label">Member (User) ID</label>
                                <input type="number" class="form-control" id="user_id" v-model.number="newIssue.user_id" required placeholder="Enter User ID">
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Issue Book</button>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Borrow Records Column -->
            <div class="col-md-8">
                <div class="card border-0 shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title mb-3">Active & Historical Borrow Records</h5>
                        <div class="table-responsive">
                            <table class="table table-striped align-middle">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>User ID</th>
                                        <th>Book Title</th>
                                        <th>Issued</th>
                                        <th>Due Date</th>
                                        <th>Returned</th>
                                        <th>Fine</th>
                                        <th>Status</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="record in borrowRecords" :key="record.id">
                                        <td>{{ record.id }}</td>
                                        <td>{{ record.user_id }}</td>
                                        <td><strong>{{ record.book_title }}</strong></td>
                                        <td><small>{{ record.issue_date }}</small></td>
                                        <td><small>{{ record.due_date }}</small></td>
                                        <td><small v-if="record.return_date">{{ record.return_date }}</small><span v-else class="text-muted">-</span></td>
                                        <td>
                                            <span v-if="record.fine_amount > 0" class="text-danger fw-bold">${{ record.fine_amount }}</span>
                                            <span v-else class="text-muted">$0</span>
                                        </td>
                                        <td>
                                            <span class="badge" :class="{
                                                'bg-warning text-dark': record.status === 'issued',
                                                'bg-success': record.status === 'returned',
                                                'bg-danger': record.status === 'overdue'
                                            }">{{ record.status }}</span>
                                        </td>
                                        <td>
                                            <button v-if="record.status === 'issued' || record.status === 'overdue'" class="btn btn-sm btn-success" @click="processReturn(record.id)">
                                                Return
                                            </button>
                                            <span v-else class="text-muted">-</span>
                                        </td>
                                    </tr>
                                    <tr v-if="borrowRecords.length === 0">
                                        <td colspan="9" class="text-center text-muted py-3">No borrow records found.</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
