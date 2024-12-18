<!-- A chat-like speech bubble. Has no default background color. -->
<template>
	<div class="text-bubble">
        <div v-if="header" class="flex items-end mb-3">
            <img class="size-8 mr-2 rounded-md" src="../assets/images/avatar.svg"/>
            <span class="italic">{{ props.header }}</span>
        </div>
        
        <p class="text-left">{{ props.text }}</p>
        <p v-if="date" class="text-right italic opacity-75">On {{ new Date(props.date).toISOString().split('T')[0] }}</p>
    </div>
</template>

<script setup>

const props = defineProps({
    "header": String, // Shown by avatar. No avatar is shown if nullish.
    "text": String, // Main text
    "date": String, // Shown at the bottom.
})

</script>

<style scoped>

.text-bubble {
    @apply rounded-lg p-3
}

</style>
