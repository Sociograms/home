<template>
  <span>
    <div class="border border-gray-200 bg-white rounded-md">
      <div v-if="theirFile"><img :src="fullname" /></div>
      <div class="p-4 border-b border-gray-200 bg-white">{{ theirQuote }}</div>
      <div class="p-4">{{ node }}</div>
    </div>
  </span>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps({
  personID: Number,
  theirQuote: String,
  node: String,
  theirFile: String,
});

const fullname = computed(() => {
  return "/src/assets/" + props.theirFile;
});

defineEmits(["mouseover", "mouseleave", "clickit"]);
</script>
