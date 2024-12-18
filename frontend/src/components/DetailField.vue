<!-- A form field component with a horizontal layout. -->
<template>
	<div class="flex my-1">
        <p>
            <span class="text-nowrap mr-2">
                <slot/> {{ label }}:
            </span>
        </p>
        <div v-if="padBetween" class="mx-auto"></div>
        <input :type="inputType" :maxlength="maxLength" :class="editableFieldClass" :placeholder="placeholder" :list="id" :readonly="readonly" v-model="model"></input>
        <!-- Necessary for browser auto-completion -->
        <datalist v-if="options" :id=id>
            <option v-for="option in options" :value="option" />
        </datalist>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    "id": String,
    "inputType": String, // HTML form input type.
    "label": String,
    "inputFieldClass": {default: "text-right", type: String}, // TODO
    "options": Array, // Auto-complete suggestions. Should be list of strings.
    "readonly": Boolean,
    "padBetween": {default: true, type: Boolean}, // Whether to add padding between the label and input field.
    "placeholder": String,
    "maxLength": Number,
})

const model = defineModel({type: String})

const editableFieldClass = computed(() => {
    const classes = {
        'details-field': true,
        'min-w-0': true,
        'flex-grow': true,
        "details-field-editable": !props.readonly,
    }
    classes[props.inputFieldClass] = true
    return classes
})

</script>

<style scoped>

.details-field {
    /* Padding is used for nicer spacing to the input field boundaries; it's declared in this field as well to prevent the text from changing position when toggling edit mode. */
    @apply px-2 bg-transparent max-h-min
}

.details-field::placeholder {
    @apply text-gray-400
}

.details-field-editable {
    @apply bg-gray-50 border border-gray-300 rounded-lg
}

/* Get rid of the date picker outside edit mode since it's for some reason invisible anyways */
input[readonly]::-webkit-calendar-picker-indicator {
    display: none;
}
input[type="date"][readonly]::-webkit-input-placeholder{ 
    visibility: hidden !important;
}

</style>
