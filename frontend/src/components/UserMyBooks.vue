<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'

const borrowRecords = ref([])
const message = ref('')
const isSuccess = ref(false)
const token = localStorage.getItem('token')

// CSV Export States
const exportMessage = ref('')
const downl = ref('')
const downR = ref(false)
let starpoll = null

const fetchMyBorrows = async () => {
    try {
        const response = await axios.get('http://localhost:5000/borrows', {
            headers: { Authorization: `Bearer ${token}` }
        })
        borrowRecords.value = response.data.all_records
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to fetch your books'
        isSuccess.value = false
    }
}

const returnBook = async (recordId) => {
    try {
        const response = await axios.put(`http://localhost:5000/admin/return/${recordId}`, {}, {
            headers: { Authorization: `Bearer ${token}` }
        })
        const fine = response.data.fine_amount || 0
        message.value = `Returned successfully. Fine: $${fine}`
        isSuccess.value = true
        fetchMyBorrows()
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to return book'
        isSuccess.value = false
    }
}

// CSV Export Methods
const triggerExport = async () => {
    try {
        const pat = await axios.get('http://localhost:5000/user/export_csv', {
            headers: { Authorization: `Bearer ${token}` }
        })
        const file_name = pat.data.file_name
        localStorage.setItem('file_name', file_name)
        exportMessage.value = 'CSV Export has been scheduled and is processing...'
        stpoll()
    } catch (err) {
        exportMessage.value = 'Failed to schedule CSV export'
    }
}

const checkdownl = async () => {
    const file_name = localStorage.getItem('file_name')
    if (!file_name || file_name === 'none') return

    try {
        const pat = await axios.get(`http://localhost:5000/user/export_csv/${file_name}`, {
            headers: { Authorization: `Bearer ${token}` },
            responseType: 'blob'
        })
        if (pat.status === 200) {
            downl.value = URL.createObjectURL(pat.data)
            downR.value = true
            exportMessage.value = 'CSV Export complete! Ready for download.'
            if (starpoll) {
                clearInterval(starpoll)
                starpoll = null
            }
        }
    } catch (e) {
        // Not ready yet
    }
}

const stpoll = () => {
    if (starpoll) clearInterval(starpoll)
    starpoll = setInterval(checkdownl, 3000)
}

const cleardownl = () => {
    localStorage.removeItem('file_name')
    downR.value = false
    exportMessage.value = ''
    if (downl.value) {
        URL.revokeObjectURL(downl.value)
        downl.value = ''
    }
}

onMounted(() => {
    fetchMyBorrows()
    const file_name = localStorage.getItem('file_name')
    if (file_name && file_name !== 'none') {
        stpoll()
    }
})

onBeforeUnmount(() => {
    if (starpoll) {
        clearInterval(starpoll)
        starpoll = null
    }
})
</script>

<template>
    <div>
        <h3 class="mb-4">My Borrowed Books & History</h3>

        <div v-if="message" class="alert mb-3" :class="isSuccess ? 'alert-success' : 'alert-danger'" role="alert">
            {{ message }}
        </div>

        <div class="row">
            <!-- Active Borrows -->
            <div class="col-12 mb-4">
                <div class="card shadow-sm border-0">
                    <div class="card-body">
                        <h5 class="card-title text-primary mb-3">Currently Borrowed</h5>
                        <div class="table-responsive">
                            <table class="table table-striped align-middle">
                                <thead>
                                    <tr>
                                        <th>Record ID</th>
                                        <th>Book Title</th>
                                        <th>Issue Date</th>
                                        <th>Due Date</th>
                                        <th>Status</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="rec in borrowRecords.filter(r => r.status === 'issued' || r.status === 'overdue')" :key="rec.id">
                                        <td>{{ rec.id }}</td>
                                        <td><strong>{{ rec.book_title }}</strong></td>
                                        <td>{{ rec.issue_date }}</td>
                                        <td>{{ rec.due_date }}</td>
                                        <td>
                                            <span class="badge" :class="rec.status === 'overdue' ? 'bg-danger' : 'bg-warning text-dark'">
                                                {{ rec.status }}
                                            </span>
                                        </td>
                                        <td>
                                            <button class="btn btn-sm btn-success" @click="returnBook(rec.id)">
                                                Return Book
                                            </button>
                                        </td>
                                    </tr>
                                    <tr v-if="borrowRecords.filter(r => r.status === 'issued' || r.status === 'overdue').length === 0">
                                        <td colspan="6" class="text-center text-muted py-3">You don't have any books currently borrowed.</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Past Borrow History -->
            <div class="col-12 mb-4">
                <div class="card shadow-sm border-0">
                    <div class="card-body">
                        <h5 class="card-title text-secondary mb-3">Borrow History</h5>
                        <div class="table-responsive">
                            <table class="table table-striped align-middle">
                                <thead>
                                    <tr>
                                        <th>Record ID</th>
                                        <th>Book Title</th>
                                        <th>Issue Date</th>
                                        <th>Due Date</th>
                                        <th>Return Date</th>
                                        <th>Fine Paid</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="rec in borrowRecords.filter(r => r.status === 'returned')" :key="rec.id">
                                        <td>{{ rec.id }}</td>
                                        <td><strong>{{ rec.book_title }}</strong></td>
                                        <td>{{ rec.issue_date }}</td>
                                        <td>{{ rec.due_date }}</td>
                                        <td>{{ rec.return_date }}</td>
                                        <td>
                                            <span v-if="rec.fine_amount > 0" class="text-danger">${{ rec.fine_amount }}</span>
                                            <span v-else class="text-muted">$0</span>
                                        </td>
                                        <td><span class="badge bg-success">returned</span></td>
                                    </tr>
                                    <tr v-if="borrowRecords.filter(r => r.status === 'returned').length === 0">
                                        <td colspan="7" class="text-center text-muted py-3">No return history found.</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Export CSV Section -->
        <hr class="my-4">
        <div class="d-flex align-items-center flex-wrap gap-3">
            <button class="btn btn-outline-primary" @click="triggerExport">Export Borrowing History (CSV)</button>
            <button v-if="downR" class="btn btn-secondary" @click="cleardownl">Clear Export</button>
        </div>

        <div v-if="exportMessage" class="alert mt-3" :class="downR ? 'alert-success' : 'alert-info'" role="alert">
            {{ exportMessage }}
            <div v-if="downR" class="mt-2">
                <a :href="downl" target="_blank" class="btn btn-success btn-sm" download="borrowing_history.csv">Download CSV</a>
            </div>
        </div>
    </div>
</template>
