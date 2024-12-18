<template>
    <div data-wow-duration="600ms" class="broadcast__inner wow fadeInUp max-lg:px-3 max-lg:py-10 lg:p-20" style="visibility: visible; animation-duration: 600ms;">
        <div :class="containerClass">
            <div class="col-12 col-xl-7">
                <div class="section__content broadcast__inner-content">
                    <h2 class="h2">{{ props.header }}</h2>
                    <div class="paragraph text-block rounded shadow-xl p-4">
                        <p class="text-left lg:text-lg">
                            {{ props.text }}
                        </p>
                    </div>
                </div>
            </div>
            <div class="col-12 col-xl-5">
                <img :src="props.img" alt="Image" class="w-100 border-indigo-600 rounded-lg">
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    "header": String,
    "text": String,
    "img": String,
    "reverse": Boolean, // If true, the image will be shown on the left instead. Has no effect for mobile layouts.
})

const containerClass = computed(() => {
    return {
        "row": true,
        "align-items-center": true,
        "items-gap-two": true,
        "flex-row-reverse": props.reverse,
    }
})

</script>

<style scoped>
.text-block {
    background: rgb(129,140,248);
    background: linear-gradient(246deg, rgba(129,140,248,1) 0%, rgba(134,103,196,1) 58%, rgba(137,144,219,1) 100%);
}
</style>