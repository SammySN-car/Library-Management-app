<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="fw-bold mb-0">My Library</h2>
        <p class="text-muted small">Search books, request to borrow, and manage returns</p>
      </div>
      <button @click="logout" class="btn btn-outline-danger btn-sm rounded-pill px-3">Logout</button>
    </div>

    <!-- Navigation Pills -->
    <ul class="nav nav-pills mb-4 pb-2 border-bottom border-secondary opacity-75">
      <li class="nav-item">
        <button class="nav-link rounded-pill px-4 py-2 me-2" :class="{ 'active': activeTab === 'search', 'btn-premium': activeTab === 'search' }" @click="activeTab = 'search'">
          Search Catalog
        </button>
      </li>
      <li class="nav-item">
        <button class="nav-link rounded-pill px-4 py-2 me-2" :class="{ 'active': activeTab === 'mybooks', 'btn-premium': activeTab === 'mybooks' }" @click="activeTab = 'mybooks'">
          My Borrowed Books
        </button>
      </li>
      <li class="nav-item">
        <button class="nav-link rounded-pill px-4 py-2" :class="{ 'active': activeTab === 'fines', 'btn-premium': activeTab === 'fines' }" @click="activeTab = 'fines'">
          Fines & History
        </button>
      </li>
    </ul>

    <!-- Dynamic Component Area -->
    <div class="glass-card p-4">
      <div v-if="activeTab === 'search'">
        <UserSearch />
      </div>
      
      <div v-if="activeTab === 'mybooks'">
        <h5 class="fw-bold mb-4">My Borrowed Books</h5>
        <UserMyBooks />
      </div>
      
      <div v-if="activeTab === 'fines'">
        <h5 class="fw-bold mb-4">Fines</h5>
        <p class="text-muted small">Fines are calculated automatically for overdue books ($1 per day). Please clear pending fines at the desk.</p>
        <div class="alert alert-info py-2 small">Check your "My Borrowed Books" tab to see active overdues.</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { clearAuth } from '../api/auth'
import UserSearch from '../components/UserSearch.vue'
import UserMyBooks from '../components/UserMyBooks.vue'

const router = useRouter()
const activeTab = ref('search')

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