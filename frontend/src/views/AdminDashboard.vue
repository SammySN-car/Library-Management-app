<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AdminBooks from '@/components/AdminBooks.vue'
import AdminDesk from '@/components/AdminDesk.vue'
import AdminMembers from '@/components/AdminMembers.vue'
import AdminReports from '@/components/AdminReports.vue'

const router = useRouter()
const currentTab = ref('books')
const token = ref('')

onMounted(() => {
    token.value = localStorage.getItem('token')
    const role = localStorage.getItem('role')
    if (!token.value || role !== 'admin') {
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
            <h2>Admin Control Panel</h2>
            <span class="badge bg-secondary">Role: Admin</span>
        </div>
        
        <nav class="nav nav-pills flex-column flex-sm-row mb-4 p-2 bg-light rounded shadow-sm">
            <button class="flex-sm-fill text-sm-center nav-link border-0" :class="{ active: currentTab === 'books' }" @click="currentTab = 'books'">Books Catalog</button>
            <button class="flex-sm-fill text-sm-center nav-link border-0" :class="{ active: currentTab === 'desk' }" @click="currentTab = 'desk'">Issue/Return Desk</button>
            <button class="flex-sm-fill text-sm-center nav-link border-0" :class="{ active: currentTab === 'members' }" @click="currentTab = 'members'">Members</button>
            <button class="flex-sm-fill text-sm-center nav-link border-0" :class="{ active: currentTab === 'reports' }" @click="currentTab = 'reports'">Summary Reports</button>
            <button class="flex-sm-fill text-sm-center nav-link border-0 text-danger" @click="logout">Logout</button>
        </nav>

        <div class="card shadow-sm">
            <div class="card-body">
                <AdminBooks v-if="currentTab === 'books'" />
                <AdminDesk v-else-if="currentTab === 'desk'" />
                <AdminMembers v-else-if="currentTab === 'members'" />
                <AdminReports v-else-if="currentTab === 'reports'" />
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
