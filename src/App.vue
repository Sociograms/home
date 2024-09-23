<template>
  <main class="container mx-auto my-8 space-y-8">
    <h1 class="text-4xl">
      Digital photography: mediation, memory and visual communication
    </h1>
    <section v-if="!isAdmin" class="min-h-96">
      <h2 class="text-2xl">Across the practices, platforms and people</h2>
      <div><SociogramCard :snodes="filteredNodesObject" :sedges="edges" /></div>
    </section>

    <RouterView />
  </main>
</template>

<script setup lang="ts">
import { onMounted, computed } from "vue";
import SociogramCard from "@/components/SociogramCard.vue";
import useNodes from "@/composables/useNodes";
import { useRoute } from "vue-router";

const { nodes, edges, nodesLoading, fetchData } = useNodes();
const route = useRoute();

onMounted(() => {
  fetchData();
});

const filteredNodes = computed(() => {
  console.log("filtering the nodes");
  if (nodesLoading.value || !nodes.value) {
    return []; // Return an empty array if loading or not an array
  }
  // Convert the object into an array and filter
  return Object.values(nodes.value).filter((node) => {
    return node.level < 3; // just the nodes that are Me and platforms ie levels 1 and 2
  });
});

// Transform the filtered array back into a nested structure
const filteredNodesObject = computed(() => {
  const filteredArray = filteredNodes.value;
  const result = {};

  filteredArray.forEach((node) => {
    result[node.name] = node; // Use the node's name as the key
  });

  return result; // Return the newly structured object
});

const isAdmin = computed(() => {
  return route.path === "/admin";
});
</script>
