import { createRouter, createWebHistory } from "vue-router";
import NotFoundView from "@/views/NotFoundView.vue";
import SelectedNodesView from "@/views/SelectedNodesView.vue";
import ChangeNodesView from "@/views/ChangeNodesView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: NotFoundView,
    },
    {
      path: "/quotes/:selectedNode",
      name: "quotesview",
      component: SelectedNodesView,
    },
    {
      path: "/admin",
      name: "adminview",
      component: ChangeNodesView,
    },
  ],
});

export default router;
