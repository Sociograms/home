import { ref } from "vue";
import alldata from "@/newdb.json";

const nodes = ref([]);
const quotes = ref([]);
const edges = ref([]);
const nodesLoading = ref(false);

function fetchData() {
  nodesLoading.value = true;

  console.log("fetch data");
  nodes.value = alldata.nodes;
  edges.value = alldata.edges;
  quotes.value = alldata.quotes;

  nodesLoading.value = false;
}

export default function useNodes() {
  return {
    nodes,
    edges,
    quotes,
    nodesLoading,
    fetchData,
  };
}
