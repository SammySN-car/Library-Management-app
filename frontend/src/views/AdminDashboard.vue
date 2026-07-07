<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="fw-bold mb-0">Admin Dashboard</h2>
        <p class="text-muted small">Manage library operations and resources</p>
      </div>
      <button @click="logout" class="btn btn-outline-danger btn-sm rounded-pill px-3">Logout</button>
    </div>

    <!-- Navigation Pills -->
    <ul class="nav nav-pills mb-4 pb-2 border-bottom border-secondary opacity-75">
      <li class="nav-item">
        <button class="nav-link rounded-pill px-4 py-2 me-2" :class="{ 'active': activeTab === 'books', 'btn-premium': activeTab === 'books' }" @click="activeTab = 'books'">
          Books
        </button>
      </li>
      <li class="nav-item">
        <button class="nav-link rounded-pill px-4 py-2 me-2" :class="{ 'active': activeTab === 'members', 'btn-premium': activeTab === 'members' }" @click="activeTab = 'members'">
          Members
        </button>
      </li>
      <li class="nav-item">
        <button class="nav-link rounded-pill px-4 py-2 me-2" :class="{ 'active': activeTab === 'desk', 'btn-premium': activeTab === 'desk' }" @click="activeTab = 'desk'">
          Issue / Return Desk
        </button>
      </li>
      <li class="nav-item">
        <button class="nav-link rounded-pill px-4 py-2" :class="{ 'active': activeTab === 'reports', 'btn-premium': activeTab === 'reports' }" @click="activeTab = 'reports'">
          Reports
        </button>
      </li>
    </ul>

    <!-- Dynamic Component Area -->
    <div class="glass-card p-4">
      <div v-if="activeTab === 'books'">
        <AdminBooks />
      </div>
      
      <div v-if="activeTab === 'members'">
        <AdminMembers />
      </div>
      
      <div v-if="activeTab === 'desk'">
        <AdminDesk />
      </div>
      
      <div v-if="activeTab === 'reports'">
        <AdminReports />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { clearAuth } from '../api/auth'
import AdminBooks from '../components/AdminBooks.vue'
import AdminMembers from '../components/AdminMembers.vue'
import AdminDesk from '../components/AdminDesk.vue'
import AdminReports from '../components/AdminReports.vue'

const router = useRouter()
const activeTab = ref('books')

const logout = () => {
  clearAuth()
  router.push('/login')
}
</script>

<style scoped>
.nav-link {
  color: var(--text-secondary);
  font-weight: 500;
  transition: all 0.2s;
}
.nav-link:hover:not(.active) {
  background: var(--surface-2);
  color: var(--text-main);
}
</style>