<!-- A searchable dropdown form component. -->
<template>
	<div class="mb-3">
        <div class="flex flex-row justify-between">
            <label for="inputField" class="block text-sm font-medium text-left ml-1 mb-2" >{{ label }} {{ required ? " *" : "" }}</label>
            <p v-if="warning" class="text-sm text-red-500 font-medium" :data-test="testId + '-warning'">{{ warning }}</p>
        </div>
        
        <Multiselect v-model="model" :options="options" :track-by="trackBy" :label="optionLabelKey" :allow-empty="allowEmpty" :searchable="canSearch" :data-test="testId"></Multiselect>
  </div>
</template>

<script setup>
import Multiselect from 'vue-multiselect'

defineProps({
    "label": String,
    "warning": String, // Shows an extra red label on the right
    "required": Boolean, // Shows a * by the label
    "options": Array, // Selectable options
    "optionLabelKey": String, // Defines which key to display as the option label if options prop is an array
    "allowEmpty": Boolean, // Whether to allow selecting no option
    "canSearch": Boolean,
    "trackBy": String, // Defines which key to use as option ID if options prop is an array
    "testId": String,
})

const model = defineModel({type: String})

</script>

<style scoped>

</style>
