<!-- A card for a question to an artist, showing its anwer and management controls. -->
<template>
	<div class="flex flex-col py-3 px-4 bg-indigo-300 rounded relative banner">
        <!-- Artist name and archive button -->
        <div class="rounded bg-white max-w-min px-3 mb-1 mx-auto">
            <p class="text-nowrap">Your question to {{ question.artist_username }}</p>
        </div>

        <!-- Show delete button on top-right on desktop -->
        <button v-if="!props.question.archived" class="btn btn-delete max-md:hidden md:absolute top-2 right-2 mx-auto" @click="$emit('archived')"><TrashIcon class="icon"/> Archive</button>

        <div class="my-1"/>

        <!-- Question -->
        <div class="flex flex-col gap-y-2">
            <ChatBubble class="ml-auto bg-indigo-400" header="You asked:" :text="props.question.question_text" :date="props.question.question_date"/>

            <!-- Response -->
            <ChatBubble v-if="props.question.response_status === 'answered'" class="mr-auto bg-indigo-500" :header="`${question.artist_username} responded:`" :text="props.question.response_text" :date="props.question.response_date"/>
            <ChatBubble v-else-if="props.question.response_status === 'rejected'" class="mr-auto bg-red-400" text="The artist rejected your question."/>
            <ChatBubble v-else-if="props.question.response_status === 'waiting'" class="mr-auto bg-gray-300" text="The artist has not yet answered your question."/>
        </div>

        <!-- Show delete button at the bottom on mobile -->
        <button v-if="!props.question.archived" class="btn btn-delete md:hidden mt-2 mx-auto" @click="$emit('archived')"><TrashIcon class="icon"/> Archive</button>
    </div>
</template>

<script setup>
import ChatBubble from '../components/ChatBubble.vue'
import { TrashIcon } from '@heroicons/vue/24/solid'



const props = defineProps({
    "question": Object,
})



defineEmits(['archived'])

</script>

<style scoped>

.btn {
    @apply font-bold py-3 px-4 rounded;
}

.btn-delete {
    @apply bg-blue-500 text-white;
}

.btn-delete:hover,
.btn-delete:focus {
    @apply bg-red-700;
}

.banner {
    background-image: url("../assets/images/broadcast-bg.png");
    @apply bg-cover
}

</style>
