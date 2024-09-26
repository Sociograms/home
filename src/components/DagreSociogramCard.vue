<template>
  <div class="h-96">
    <v-network-graph
      :zoom-level="0.1"
      :nodes="props.snodes"
      :edges="props.sedges"
      :configs="configs"
      :layouts="data.layouts"
    >
    </v-network-graph>
  </div>
</template>
<script setup lang="ts">
import { ref, reactive } from "vue";
import * as vNG from "v-network-graph";
import dagre from "dagre/dist/dagre.min.js"


import { ForceLayout } from "v-network-graph/lib/force-layout";
import type {
  ForceNodeDatum,
  ForceEdgeDatum,
} from "v-network-graph/lib/force-layout";

const nodeSize = 40

/*
const props = defineProps({
  snodes: [],
  sedges: [],
});
*/

const props = defineProps<{
  snodes: {
    [key: string]: {
      name: string;
      type: string;
      label: string;
      level: number;
      color: string;
      x?: number; // Optional
      y?: number; // Optional
    };
  };
  sedges: Record<string, { source: string; target: string }> | Array<{ source: string; target: string }>;
}>();

const data = reactive({
  layouts: {
    nodes: {}
  }
});
const graph = ref<vNG.VNetworkGraphInstance>()

const configs = reactive(
  vNG.defineConfigs({
  view: {
    autoPanAndZoomOnLoad: "fit-content",
    zoomEnabled: true,
    onBeforeInitialDisplay: () => layout("TB"),
    },
    node: {
      normal: {
        type: (n) =>
          n.type === "Person" || n.type === "Recipients" ? "circle" : "rect",
        color: (n) => n.color,
        radius: (n) => (n.label === "Me" ? 50 : 20),
      },
      selectable: 1,
      label: {
        fontSize: (n) => (n.label === "Me" ? 20 : 11),
        direction: (n) => (n.label === "Me" ? "center" : "south"),
      },
    },
  }),
);


function layout(direction: "TB" | "LR") {
  if (Object.keys(props.snodes).length <= 1 || props.sedges.length === 0) {
    return;
  }

  const g = new dagre.graphlib.Graph();
  g.setGraph({
    rankdir: direction,
    nodesep: nodeSize,
    edgesep: nodeSize,
    ranksep: nodeSize * 10,
  });
  g.setDefaultEdgeLabel(() => ({}));

  // Add nodes to the graph
  Object.entries(props.snodes).forEach(([nodeId, node]) => {
    g.setNode(nodeId, {
      label: node.name,
      width: nodeSize,
      height: nodeSize,
      x: node.x || 0,
      y: node.y || 0,
    });
  });

  // Add edges to the graph
  Object.values(props.sedges).forEach(edge => {
    g.setEdge(edge.source, edge.target);
  });

  // Perform layout calculation
  dagre.layout(g);

  // Construct data.layouts.nodes
  data.layouts.nodes = {}; // Initialize or reset it
  g.nodes().forEach((nodeId: string) => {
    const graphNode = g.node(nodeId);
    if (graphNode) { // Check if the node exists
      const { x, y } = graphNode;
      data.layouts.nodes[nodeId] = { x, y };
    } else {
      console.warn(`Node ${nodeId} not found in the graph.`);
    }
  });
}

function updateLayout(direction: "TB" | "LR") {
  const graph = ref(null); // Define a ref if you plan to use it
  graph.value?.transitionWhile(() => {
    layout(direction);
  });
}
</script>

<style>
.graph {
  width: 880px;
  height: 600px;
  border: 1px solid #000;
}
</style>