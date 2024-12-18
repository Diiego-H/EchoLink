<template>
    <div class="w-100">
        <draggable v-model="internalSongs" group="songs" @start="dragging=true" @end="dragging=false" item-key="song_id" handle=".handle" @update="$emit('reordered')">
            <template #item="{element}">
                <SongItem class="my-1" :song="element" :show-handle="props.editable" :show-delete="props.editable" :prefix="getSongPrefix(element)" @removed="removeSong($event)"></SongItem>
            </template>
        </draggable>
    </div>
</template>

<script setup>
import draggable from 'vuedraggable'
import SongItem from '../components/SongItem.vue'
import { ref, computed } from 'vue';

const songs = defineModel({type: Array})

const emit = defineEmits(['removed', 'reordered'])

const props = defineProps({
    "editable": Boolean, // Whether songs can be reordered and deleted. Adding songs is an external responsibility.
    value: {
        type: Array,
        default: () => []
    }
})

const dragging = ref(false)

const internalSongs = computed({
    get(){
        return songs.value?.length ? songs.value : props.value;
    },
    set(newValue){
        if(songs.value?.length){
            songs.value = newValue; // Update v-model
        } 
        else{
            emit('input', newValue); // Emit input for :value
        }
    }
})

function getSongPrefix(song) {
    const index = internalSongs.value.indexOf(song) + 1
    return `${index}.`
}

function removeSong(song) {
    // TODO maybe prompt the user first?
    internalSongs.value.splice(internalSongs.value.indexOf(song), 1)
    emit('removed', song)
}

</script>

<style scoped>

</style>
