<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const members = ref([])
const message = ref('')
const isSuccess = ref(false)
const token = localStorage.getItem('token')

const fetchMembers = async () => {
    try {
        const response = await axios.get('http://localhost:5000/admin/members', {
            headers: { Authorization: `Bearer ${token}` }
        })
        members.value = response.data.all_users
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to fetch members'
        isSuccess.value = false
    }
}

onMounted(() => {
    fetchMembers()
})
</script>

<template>
    <div>
        <h3 class="mb-4">Registered Library Members</h3>

        <div v-if="message" class="alert mb-3" :class="isSuccess ? 'alert-success' : 'alert-danger'" role="alert">
            {{ message }}
        </div>

        <div class="table-responsive">
            <table class="table table-striped table-hover align-middle">
                <thead class="table-dark">
                    <tr>
                        <th>Member ID</th>
                        <th>Full Name</th>
                        <th>Email ID</th>
                        <th>Address</th>
                        <th>Pincode</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in members" :key="user.id">
                        <td>{{ user.id }}</td>
                        <td><strong>{{ user.full_name }}</strong></td>
                        <td><code>{{ user.email_id }}</code></td>
                        <td>{{ user.address }}</td>
                        <td>{{ user.pincode }}</td>
                    </tr>
                    <tr v-if="members.length === 0">
                        <td colspan="5" class="text-center text-muted py-4">No members registered yet.</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
