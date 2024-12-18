<!-- Small panel for displaying error messages. -->
<template>
	<div class="content-block max-w-sm mx-auto" data-test="container-error">
        <p>{{ props.header }}</p>
        <p>{{ props.reason }}</p>
        <RouterLink to="/">Return to homepage</RouterLink>
    </div>
</template>

<script setup>

const props = defineProps({
    "header": String,
    "reason": String,
})

</script>

<style scoped>

</style>
