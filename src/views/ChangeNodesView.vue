<template>
  <h1>
    Secret Jasmine View to change the Nodes and their Edges (ie connectors)
  </h1>

  <div class="min-h-96">
    <v-network-graph
      :zoom-level="0.5"
      :nodes="nodes"
      :edges="edges"
      :layouts="layouts"
      :configs="configs"
      :event-handlers="eventHandlers"
    >
    </v-network-graph>
  </div>
</template>

<script setup lang="ts">
import useNodes from "@/composables/useNodes";
import SociogramCard from "@/components/SociogramCard.vue";

import { ref, reactive } from "vue";
import * as vNG from "v-network-graph";

import { ForceLayout } from "v-network-graph/lib/force-layout";
import type {
  ForceNodeDatum,
  ForceEdgeDatum,
} from "v-network-graph/lib/force-layout";

const { nodes, edges, nodesLoading } = useNodes();

const configs = reactive(
  vNG.defineConfigs({
    view: {
      layoutHandler: new ForceLayout({
        positionFixedByDrag: false,
        positionFixedByClickWithAltKey: true,
        createSimulation: (d3, nodes, edges) => {
          // d3-force parameters
          const forceLink = d3
            .forceLink<ForceNodeDatum, ForceEdgeDatum>(edges)
            .id((d) => d.id);
          return d3
            .forceSimulation(nodes)
            .force("edge", forceLink.distance(80).strength(0.05))
            .force("charge", d3.forceManyBody().strength(-500))
            .force("center", d3.forceCenter().strength(0.05))
            .alphaMin(0.001);
        },
      }),
    },
    node: {
      normal: {
        type: (n) => (n.label === "Me" ? "circle" : "rect"),
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
</script>
