<template>
  <div class="row justify-content-center align-items-center py-5">
    <div class="col-md-6">
      <div class="glass-card p-5">
        <div class="text-center mb-4">
          <h2 class="fw-bold">Create Account</h2>
          <p class="text-muted">Join the Library Management system</p>
        </div>
        
        <form @submit.prevent="handleSignup">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label text-secondary small fw-bold">Full Name</label>
              <input type="text" v-model="form.name" class="form-control form-control-premium py-2" required placeholder="John Doe">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label text-secondary small fw-bold">Email address</label>
              <input type="email" v-model="form.email" class="form-control form-control-premium py-2" required placeholder="john@example.com">
            </div>
          </div>
          
          <div class="mb-3">
            <label class="form-label text-secondary small fw-bold">Address</label>
            <input type="text" v-model="form.address" class="form-control form-control-premium py-2" required placeholder="123 Library St, City">
          </div>
          
          <div class="mb-4">
            <label class="form-label text-secondary small fw-bold">Password</label>
            <input type="password" v-model="form.password" class="form-control form-control-premium py-2" required placeholder="••••••••">
          </div>
          
          <div class="d-grid mb-3">
            <button type="submit" class="btn btn-premium py-2 fw-bold" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              Sign Up
            </button>
          </div>
          
          <div v-if="error" class="alert alert-danger py-2 text-center small mb-0 rounded">
            {{ error }}
          </div>
          <div v-if="success" class="alert alert-success py-2 text-center small mb-0 rounded">
            {{ success }}
          </div>
        </form>
        
        <div class="text-center mt-4 pt-3 border-top border-secondary opacity-50">
          <p class="small text-muted mb-0">Already have an account? <router-link to="/login" class="text-primary fw-bold text-decoration-none">Sign in</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/client'

const router = useRouter()
const form = ref({
  name: '',
  email: '',
  address: '',
  password: ''
})

const error = ref('')
const success = ref('')
const loading = ref(false)

const handleSignup = async () => {
  error.value = ''
  success.value = ''
  loading.value = true
  
  try {
    await api.post('/api/signup', {
      ...form.value,
      role: 'user' // Library system default
    })
    
    success.value = 'Account created successfully! Redirecting...'
    setTimeout(() => {
      router.push('/login')
    }, 1500)
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to register'
  } finally {
    loading.value = false
  }
}
</script>