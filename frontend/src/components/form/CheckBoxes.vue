<template>
    <div class="flex items-center mb-4">
        <!-- Cannot set border on checkbox inputs directly -->
        <div class="rounded border-3 border-indigo-300">
            <input id="checkbox" type="checkbox" :value="checked" @change="$emit('changed', $event.target.checked)" class="w-5 h-5" :data-test="testId">
        </div>
        <!-- Clicking label interacts with checkbox; best to disable select so it doesn't happen by accident -->
        <label for="checkbox" class="ms-2 text-sm font-medium unselectable">{{ label }}</label>
    </div>
</template>

<script setup>
defineProps({
    "label": String,
    "checked": Boolean,
    "testId": String,
})
</script>

<style scoped>
input[type="checkbox"] {
accent-color: hidden; /* Not a valid value, but "transparent" doesn't work to accomplish this on chromium */
}
</style>
