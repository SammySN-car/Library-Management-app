<template>
  <div>
    <h5 class="fw-bold mb-3">Manage Members</h5>
    <div class="table-responsive">
      <table class="table align-middle">
        <thead class="table-light">
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Joined</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="member in members" :key="member.id">
            <td class="fw-bold">{{ member.name }}</td>
            <td>{{ member.email }}</td>
            <td>{{ member.created_at ? new Date(member.created_at).toLocaleDateString() : 'N/A' }}</td>
            <td>
              <span :class="member.is_active ? 'badge bg-success' : 'badge bg-danger'">
                {{ member.is_active ? 'Active' : 'Blocked' }}
              </span>
            </td>
            <td>
              <button 
                class="btn btn-sm" 
                :class="member.is_active ? 'btn-outline-danger' : 'btn-outline-success'"
                @click="toggleStatus(member)"
              >
                {{ member.is_active ? 'Block' : 'Unblock' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/client'

const members = ref([])

const fetchMembers = async () => {
  try {
    const res = await api.get('/api/members')
    members.value = res.data.data
  } catch (err) {
    console.error(err)
  }
}

const toggleStatus = async (member) => {
  try {
    await api.put(`/api/members/${member.id}`, { is_active: !member.is_active })
    fetchMembers()
  } catch (err) {
    alert(err.response?.data?.message || 'Error updating member')
  }
}

onMounted(fetchMembers)
</script>