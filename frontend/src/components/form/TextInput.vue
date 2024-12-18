<template>
	<div class="mb-3">
        <div class="flex flex-row justify-between">
            <label for="inputField" class="block text-sm font-medium text-left ml-1 mb-2" >{{ label }} {{ required ? " *" : "" }}</label>
            <p v-if="warning" class="text-sm text-red-500 font-medium" :data-test="testId + '-warning'">{{ warning }}</p>
        </div>
        
        <textarea v-if="multiline" ref="input" id="inputField" cols="999999" autocomplete="off" autocorrect="on" :maxlength="maxLength" :placeholder="placeholder" class="field" @change="$emit('changed', $event.target.value)" @keyup="$emit('changed', $event.target.value)" required :data-test="testId">{{ value }}</textarea>
        <input v-else ref="input" :type="inputType" id="inputField" class="field" :placeholder="placeholder" :pattern="pattern" @change="$emit('changed', $event.target.value)" :maxlength="maxLength" :value="value" @keyup="$emit('changed', $event.target.value)" required :data-test="testId" /> <!-- Emit event also on key release (usually it's only on submit) -->
  </div>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
    "label": String,
    "placeholder": String,
    "inputType": String, // HTML <input> form type
    "pattern": String, // Form pattern to enforce
    "warning": String, // Shows an extra red label on the right
    "required": Boolean, // Shows a * by the label
    "multiline": Boolean, // If true, a textarea will be used for input instead.
    "maxLength": Number,
    "value": String,
    "testId": String,
})

const input = ref(null)
function focus(){
  input.value.focus()
}

defineExpose({focus})
</script>

<style scoped>
input {
  @apply focus:ring-blue-50 bg-indigo-100 border-indigo-200 placeholder-gray-400 text-black focus:border-blue-500
}
input::placeholder {
  @apply text-gray-500
}

.field {
  @apply p-2.5 bg-gray-50 border border-gray-300 text-sm rounded-lg block w-full
}


</style>
