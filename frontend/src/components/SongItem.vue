<template>
	<div class="rounded">
        <div class="flex items-center echolink-container">

            <!-- Song icon (would be ex. album cover) -->
            <div class="flex size-10 min-w-10 rounded bg-indigo-400 max-lg:hidden"> <!-- Not shown on mobile due to space concerns -->
                <MusicalNoteIcon class="icon-h5 my-auto mx-auto"/>
            </div>

            <!-- Song name and artist -->
            <div class="lg:mx-3 text-left flex flex-col max-sm:overflow-scroll sm:overflow-clip max-sm:max-w-80 sm:max-w-96">
                <router-link :to="`/songs/${song.song_id}`" class="font-bold text-lg">{{ song.title }}</router-link>
                <router-link :to="`/users/${song.artist_name}`" class="text-sm text-gray-500">{{ song.artist_name }}</router-link>
            </div>

            <div class="mx-auto"></div>

            <!-- Genre -->
            <span v-if="!showHandle && !showDelete" class="mx-3 text-nowrap overflow-ellipsis uppercase" v-tooltip="'Genre'" >{{  song.genre.toUpperCase().split(" ").slice(-2).join(" ") }}</span>

            <!-- Edition controls -->
            <Bars3Icon v-if="showHandle" class="icon handle mx-3 min-w-8" />
            <button v-if="showDelete" class="btn btn-delete text-nowrap p-2 h-full max-w-fit" @click="$emit('removed', song)">
                <TrashIcon class="icon-h5" />
            </button>
        </div>
    </div>
</template>

<script setup>
import { MusicalNoteIcon, TrashIcon, Bars3Icon } from '@heroicons/vue/24/solid'
import { computed } from 'vue'
defineProps({
    song: Object, // TODO adjust all usages once specs are final
    "showHandle": Boolean, // Whether to show a drag handle.
    "showDelete": Boolean, // Whether to show a delete button.
    "prefix": String, // String to prefix before artist and title.
})


// TODO readd once we add song durations to API
// const duration = computed(() => {
//     let seconds = `${props.song.duration % 60}`
//     seconds = seconds.padStart(3 - seconds.length, 0)
//     return `${Math.floor(props.song.duration / 60)}:${seconds}` // Assumes duration is in seconds
// })

</script>

<style scoped>

.btn {
    @apply font-bold rounded;
}

.btn-delete {
    @apply bg-blue-500 text-white;
}

.btn-delete:hover,
.btn-delete:focus {
    @apply bg-red-700;
}

.handle {
    cursor: pointer;
}

/* Capitalize genre */
.uppercase {
    text-transform: capitalize;
}

/* Adjust spacing and font sizes */
.font-bold {
    font-weight: bold;
}

.text-lg {
    font-size: 1.125rem; /* Larger font for song title */
}

.text-sm {
    font-size: 0.875rem; /* Smaller font for artist name */
}

.text-gray-500 {
    color: #6b7280; /* Subtle gray for artist name */
}

</style>