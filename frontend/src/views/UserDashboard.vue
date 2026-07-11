<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import UserSearch from '@/components/UserSearch.vue'
import UserMyBooks from '@/components/UserMyBooks.vue'

const router = useRouter()
const currentTab = ref('search')
const token = ref('')

onMounted(() => {
    token.value = localStorage.getItem('token')
    const role = localStorage.getItem('role')
    if (!token.value || role !== 'user') {
        router.push('/')
    }
})

const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    localStorage.removeItem('id')
    router.push('/')
}
</script>

<template>
    <div class="container mt-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h2>Library Dashboard</h2>
            <span class="badge bg-primary">Member Access</span>
        </div>
        
        <nav class="nav nav-pills flex-column flex-sm-row mb-4 p-2 bg-light rounded shadow-sm">
            <button class="flex-sm-fill text-sm-center nav-link border-0" :class="{ active: currentTab === 'search' }" @click="currentTab = 'search'">Search & Borrow</button>
            <button class="flex-sm-fill text-sm-center nav-link border-0" :class="{ active: currentTab === 'mybooks' }" @click="currentTab = 'mybooks'">My Books & History</button>
            <button class="flex-sm-fill text-sm-center nav-link border-0 text-danger" @click="logout">Logout</button>
        </nav>

        <div class="card shadow-sm">
            <div class="card-body">
                <UserSearch v-if="currentTab === 'search'" />
                <UserMyBooks v-else-if="currentTab === 'mybooks'" />
            </div>
        </div>
    </div>
</template>

<style scoped>
.nav-link {
    cursor: pointer;
    font-weight: 500;
}
.nav-link.active {
    background-color: #0d6efd !important;
    color: white !important;
}
</style>
