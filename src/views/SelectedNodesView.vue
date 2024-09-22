<template>
  <h2 class="text-2xl">
    Individuals' social sharing practices through
    {{ $route.params.selectedNode }}
  </h2>

  <section>
    <div><SociogramCard :snodes="filteredNodes" :sedges="edges" /></div>
  </section>
  <section>
    <div v-if="filteredQuotes" class="grid grid-cols-2 gap-8">
      <TextCard
        v-for="(quote, index) in filteredQuotes"
        :key="index"
        :personID="quote.PersonID"
        :theirQuote="quote.Quote"
        :node="quote.Node"
        :theirFile="quote.File"
      />
    </div>
    <div v-else>
      <p>No quotes to show yet, please click on a node from the graph above</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import TextCard from "@/components/TextCard.vue";
import { useRoute } from "vue-router";
import useNodes from "@/composables/useNodes";
import SociogramCard from "@/components/SociogramCard.vue";

const route = useRoute();
const { nodes, quotes, edges, nodesLoading } = useNodes();

// Build adjacency list
const buildAdjacencyList = (edges) => {
  const adjacencyList = {};
  for (const key in edges) {
    const edge = edges[key];
    if (edge && edge.source && edge.target) {
      if (!adjacencyList[edge.source]) {
        adjacencyList[edge.source] = [];
      }
      adjacencyList[edge.source].push(edge.target);
    }
  }
  return adjacencyList;
};

// Watch for edges and build adjacency list
const adjacencyList = ref({});

watch(
  edges,
  (newEdges) => {
    adjacencyList.value = buildAdjacencyList(newEdges);
  },
  { immediate: true },
);

// Find connected nodes (children and grandchildren)
const findConnectedNodes = (node, depth = 2) => {
  const visited = new Set();
  const results = [];

  const traverse = (currentNode, currentDepth) => {
    if (currentDepth > depth || visited.has(currentNode)) return;
    visited.add(currentNode);
    const children = adjacencyList.value[currentNode] || [];
    results.push(...children);
    children.forEach((child) => traverse(child, currentDepth + 1));
  };

  traverse(node, 1); // Start from depth 1
  return results;
};

const connectedNodes = computed(() => {
  const selectedNode = route.params.selectedNode;
  if (!selectedNode) return [];
  return findConnectedNodes(selectedNode);
});

const filteredNodes = computed(() => {
  if (nodesLoading.value || !nodes.value) return {};

  const result = {};
  Object.entries(nodes.value).forEach(([key, node]) => {
    if (connectedNodes.value.includes(node.name)) {
      result[key] = { ...node };
    }
  });

  return result;
});

const filteredQuotes = computed(() => {
  if (!connectedNodes) {
    return []; // Return an empty array if selectedNode is not defined
  }
  return quotes.value
    .filter((q) => connectedNodes.value.includes(q.Node))
    .sort((a, b) => a.Quote.length - b.Quote.length);
});
</script>
