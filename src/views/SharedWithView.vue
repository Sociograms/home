<template></template>

<script setup lang="ts">
import { useRoute } from "vue-router";
import useNodes from "@/composables/useNodes";
const route = useRoute();
const { edges } = useNodes();
</script>
