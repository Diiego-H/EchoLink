<template>
    <div class="home-two-light home-light container">
        <HeaderComponent />
        <!-- Set a fixed width for the container -->
        <div class="form-container mx-auto p-4 mt-8 border-3 rounded-lg border-indigo-100 bg-indigo-200">
            <div class="mb-3">
                <h2>Register</h2>
                <p>Already got an account? <RouterLink to="/login">Log-in instead.</RouterLink></p>
            </div>

            <!-- Form field container -->
            <div class="px-4 mx-auto">
                <!-- Basic info -->
                <TextInput label="Username" :required="true" placeholder="Username" input-type="text" :value="username" @changed="username = $event" :warning="usernameWarning" :test-id="'field-username'"></TextInput>
                <TextInput label="E-mail" :required="true" placeholder="example@example.com" input-type="email" :value="email" @changed="email = $event" :warning="emailWarning" :test-id="'field-email'"></TextInput>
                
                <hr class="h-divider"/>

                <!-- Password -->
                <TextInput label="Password" :required="true" placeholder="" input-type="password" :value="password" @changed="password = $event" :warning="passwordWarning" :test-id="'field-password'"></TextInput>
                <TextInput label="Confirm password" :required="true" placeholder="" input-type="password" :value="passwordConfirmation" @changed="passwordConfirmation = $event" :warning="passwordConfirmationWarning" :test-id="'field-passwordconfirmation'"></TextInput>
                
                <hr class="h-divider"/>

                <!-- Role dropdown -->
                <div class="mb-4">
                    <div class="flex justify-between items-center">
                        <label for="role" class="block text-sm font-medium text-gray-900">Role <span class="text-black-600">*</span></label>                        
                        <p v-if="roleWarning" class="text-sm text-red-600 font-medium mt-1">{{ roleWarning }}</p>
                    </div>
                    <div class="mt-1">
                        <!-- Dropdown for role selection -->
                        <select
                            id="role"
                            v-model="role"
                            class="w-full px-3 py-2 border bg-gray-50 border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                            :data-test="'field-role'"
                        >
                            <option value="Listener">Listener</option>
                            <option value="Artist">Artist</option>
                        </select>
                    </div>
                </div>

                <hr class="h-divider"/>

                <Checkbox label="I agree to the terms of service *" :checked="termsOfServiceChecked" @changed="termsOfServiceChecked = $event" :test-id="'checkbox-tos'"></Checkbox>
            </div>

            <button class="btn btn--primary w-100 w-md-60" :disabled="!canRegister" @click="register" :data-test="'button-register'">Register</button>
        </div>

        <FooterComponent class="footer-light mx-10" />
    </div>
</template>

<script setup>
import HeaderComponent from '../components/HeaderComponent.vue';
import FooterComponent from '../components/FooterComponent.vue';
import TextInput from '../components/form/TextInput.vue';
import Checkbox from '../components/form/CheckBoxes.vue';
import UserService from '../services/user.js'
import Swal from 'sweetalert2'
import Toast from '../utilities/toast.js'
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const passwordConfirmation = ref('')
const role = ref('Listener')  // Set default value to 'Listener'
const termsOfServiceChecked = ref(false)

const roles = ["Artist", "Listener"].sort()

function register() {
    UserService.registerAccount(username.value, email.value, password.value, role.value.toLowerCase()).then(() => {
        Toast.fire({
            title: 'Registration successful!',
            icon: 'success',
        })
        // Login automatically
        UserService.loginAccount(email.value, password.value).then(() => {
            router.push('/') // Go to homepage
        }).catch((err) => {
            Swal.fire({
                title: 'Login failed',
                text: (err.response !== null) ? err.response.data.detail : err.message,
                icon: 'error',
            })
        })
    }).catch((err) => {
        Swal.fire({
            title: 'Registration failed',
            text: (err.response !== null) ? err.response.data.detail : err.message,
            icon: 'error',
        })
    })
}

const isUsernameValid = computed(() => {
    // 4-16 characters, can include digits and underscore
    const regex = RegExp(/^([a-zA-Z0-9_]{4,16})$/)
    return regex.test(username.value)
})

const isEmailValid = computed(() => {
    // Pattern source: https://stackoverflow.com/a/46181
    const regex = RegExp(/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)
    return regex.test(email.value)
})

const isPasswordValid = computed(() => {
    return password.value.length >= 8 // 8+ characters
})

const passwordMatches = computed(() => {
    return password.value === passwordConfirmation.value
})

const isRoleValid = computed(() => {
    return roles.includes(role.value);
})

const canRegister = computed(() => {
    return isUsernameValid.value && isEmailValid.value && isPasswordValid.value && passwordMatches.value && termsOfServiceChecked.value
})

// Warnings for invalid fields
const usernameWarning = computed(() => {
    return (username.value !== '' && !isUsernameValid.value) ? 'Must be 4-16 letters, digits or underscores' : null
})
const emailWarning = computed(() => {
    return (email.value !== '' && !isEmailValid.value) ? 'Must be a valid address' : null
})
const passwordWarning = computed(() => {
    return (password.value !== '' && !isPasswordValid.value) ? 'Must be 8+ characters' : null
})
const passwordConfirmationWarning = computed(() => {
    return (passwordConfirmation.value !== '' && !passwordMatches.value) ? 'Passwords must match' : null
})
const roleWarning = computed(() => {
    return (role.value !== '' && !isRoleValid.value) ? 'That\'s not an option' : null
})
</script>

<style scoped>
.container {
    width: 100vw;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start; /* Align items to the top */
    min-height: 100vh; /* Ensure the container takes the full height of the viewport */
}

.form-container {
    width: 600px;
    box-sizing: border-box; /* Include padding and border in the element's total width and height */
    margin-top: 50px; /* Add some margin to push the form down slightly from the header */
}

.footer-light {
    width: 100vw;
}

@media (max-width: 768px) {
    .form-container {
        width: 90vw; /* Full viewport width for small screens */
        height: auto; /* Full viewport height for small screens */
        margin-top: 10vh; /* Remove margin for full screen effect */
        border-radius: 0; /* Remove border radius for full screen effect */
    }
}
</style>
