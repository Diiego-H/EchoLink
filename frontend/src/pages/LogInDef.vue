<template>
    <div class="home-two-light home-light container">

        <HeaderComponent />
        <!-- Set a fixed width for the container -->
        <div class="form-container mx-auto p-4 mt-8 border-3 rounded-lg border-indigo-100 bg-indigo-200">
            <div class="mb-3">
                <h2>Log In</h2>
                <p>Don't have an account? <RouterLink to="/register">Register instead.</RouterLink></p>
            </div>


            <!-- Form field container -->
            <div class="px-4 mx-auto">
                <!-- E mail -->
                <TextInput label="E-mail" @keyup.enter="focusSecondText" :required="true" placeholder="example@example.com" input-type="email" :value="email" @changed="email = $event" :warning="emailWarning" :test-id="'field-email'" ref="InputEmail"></TextInput>
                <!-- Password -->
                <TextInput label="Password" @keyup.enter="logInEnter" :required="true" placeholder="" input-type="password" :value="password" @changed="password = $event" :warning="passwordWarning" :test-id="'field-password'" ref="InputPassword"></TextInput>
            </div>

            <hr class="h-divider"/>


            <button class="btn btn--primary w-100 w-md-60" :disabled="!canLogIn" @click="logIn" :data-test="'button-login'">Log In</button>

        </div>

        <FooterComponent class="footer-light mx-10" />
    </div>
</template>

<script setup>
import HeaderComponent from '../components/HeaderComponent.vue';
import FooterComponent from '../components/FooterComponent.vue';
import TextInput from '../components/form/TextInput.vue';
import UserService from '../services/user.js'
import Swal from 'sweetalert2'
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()
const Toast = Swal.mixin({
  toast: true,
  position: 'top',
  iconColor: 'white',
  customClass: {
    popup: 'colored-toast',
  },
  showConfirmButton: false,
  timer: 1500,
  timerProgressBar: false,
})

const email = ref('')
const password = ref('')


const InputPassword = ref(null)
const InputEmail = ref(null)


function focusSecondText(){
    InputPassword.value.focus()
}


function logIn(){
    UserService.loginAccount(email.value, password.value).then(() => {
        Toast.fire({
            title: 'Log in successful!',
            icon: 'success',
        });
        router.push('/') 
    }).catch((err) => {
        Swal.fire({
            title: 'Log in failed',
            text: 'Reason: ' + err.response.data.detail,
            icon: 'error',
        })
    })
}


const isEmailValid = computed(() => {
    // Pattern source: https://stackoverflow.com/a/46181
    const regex = RegExp(/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)
    return regex.test(email.value)
})

const isPasswordValid = computed(() => {
    return password.value.length >= 8 // 8+ characters
})

const canLogIn = computed(() => {
    return isEmailValid.value && isPasswordValid.value 
})

// Warnings for invalid fields
const emailWarning = computed(() => {
    return (email.value !== '' && !isEmailValid.value) ? 'Must be a valid address' : null
})
const passwordWarning = computed(() => {
    return (password.value !== '' && !isPasswordValid.value) ? 'Must be 8+ characters' : null
})


function logInEnter(){
    if (canLogIn) logIn()
}

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