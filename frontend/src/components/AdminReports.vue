<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Chart, BarController, BarElement, CategoryScale, LinearScale, PieController, ArcElement, Tooltip, Legend } from 'chart.js'

Chart.register(BarController, BarElement, CategoryScale, LinearScale, PieController, ArcElement, Tooltip, Legend)

const genreChartRef = ref(null)
const popularChartRef = ref(null)
const overdueList = ref([])
const totalFine = ref(0)
const message = ref('')
const isSuccess = ref(false)
const token = localStorage.getItem('token')

const genreChartInstance = ref(null)
const popularChartInstance = ref(null)

const fetchReports = async () => {
    try {
        const response = await axios.get('http://localhost:5000/admin/reports', {
            headers: { Authorization: `Bearer ${token}` }
        })
        const data = response.data
        overdueList.value = data.overdue_list || []
        totalFine.value = data.total_fine || 0

        // Genre Chart data
        const genres = data.genre_data || []
        if (genres.length > 0) {
            if (genreChartInstance.value) genreChartInstance.value.destroy()
            genreChartInstance.value = new Chart(genreChartRef.value, {
                type: 'pie',
                data: {
                    labels: genres.map(g => g.genre),
                    datasets: [{
                        label: 'Books by Genre',
                        data: genres.map(g => g.count),
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.7)',
                            'rgba(54, 162, 235, 0.7)',
                            'rgba(255, 206, 86, 0.7)',
                            'rgba(75, 192, 192, 0.7)',
                            'rgba(153, 102, 255, 0.7)',
                            'rgba(255, 159, 64, 0.7)'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            })
        }

        // Popular Books Chart data
        const popular = data.popular_books || []
        if (popular.length > 0) {
            if (popularChartInstance.value) popularChartInstance.value.destroy()
            popularChartInstance.value = new Chart(popularChartRef.value, {
                type: 'bar',
                data: {
                    labels: popular.map(b => b.title),
                    datasets: [{
                        label: 'Borrows Count',
                        data: popular.map(b => b.borrow_count),
                        backgroundColor: 'rgba(54, 162, 235, 0.7)',
                        borderColor: 'rgb(54, 162, 235)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { precision: 0 }
                        }
                    }
                }
            })
        }
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to fetch report data'
        isSuccess.value = false
    }
}

onMounted(() => {
    fetchReports()
})
</script>

<template>
    <div>
        <h3 class="mb-4">Library Analytics & Reports</h3>

        <div v-if="message" class="alert mb-3" :class="isSuccess ? 'alert-success' : 'alert-danger'" role="alert">
            {{ message }}
        </div>

        <!-- Fines Info -->
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="card bg-success text-white shadow-sm border-0">
                    <div class="card-body py-4">
                        <h6 class="card-subtitle mb-2 text-uppercase text-white-50">Total Fine Collected</h6>
                        <h2 class="card-title mb-0">${{ totalFine }}</h2>
                    </div>
                </div>
            </div>
            <div class="col-md-8">
                <div class="card shadow-sm border-0 border-start border-danger border-4">
                    <div class="card-body">
                        <h5 class="card-title text-danger">Overdue Books (Outstanding Alerts)</h5>
                        <div class="table-responsive" style="max-height: 200px; overflow-y: auto;">
                            <table class="table table-sm table-striped">
                                <thead>
                                    <tr>
                                        <th>User ID</th>
                                        <th>Book Title</th>
                                        <th>Due Date</th>
                                        <th>Fine Accrued</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="rec in overdueList" :key="rec.id">
                                        <td>{{ rec.user_id }}</td>
                                        <td>{{ rec.title }}</td>
                                        <td><code class="text-danger">{{ rec.due_date }}</code></td>
                                        <td>${{ rec.fine_amount || 0 }}</td>
                                    </tr>
                                    <tr v-if="overdueList.length === 0">
                                        <td colspan="4" class="text-muted text-center py-2">No overdue books at present.</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Charts Row -->
        <div class="row">
            <div class="col-md-6 mb-4">
                <div class="card shadow-sm border-0">
                    <div class="card-body">
                        <h5 class="card-title mb-3">Popular Books</h5>
                        <div style="height: 300px;">
                            <canvas ref="popularChartRef"></canvas>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6 mb-4">
                <div class="card shadow-sm border-0">
                    <div class="card-body">
                        <h5 class="card-title mb-3">Genre Distribution</h5>
                        <div style="height: 300px;">
                            <canvas ref="genreChartRef"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
