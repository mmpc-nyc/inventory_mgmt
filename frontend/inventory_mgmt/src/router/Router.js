import {createRouter, createWebHistory} from "vue-router"
import adminRoutes from "@/router/admin/RouterAdmin";

const baseRoutes = [
    {
        path: "/",
        name: "Home",
        component: () => import(/* webpackChunkName: "admin" */ "@/views/admin/TheAdmin"),
    },
    {
        path: "/my_equipment",
        name: "my_equipment",
        component: () => import(/* webpackChunkName: "my_equipment" */ "@/views/inventory/MyEquipment.vue")
    },
    {
        path: "/my_orders",
        name: "my_orders",
        component: () => import(/* webpackChunkName: "my_orders" */ "@/views/inventory/MyOrders.vue")
    },
    {
        path: "/equipment_collect",
        name: "equipment_collect",
        component: () => import(/* webpackChunkName: "equipment_collect" */ "@/views/inventory/EquipmentCollect")
    },
    {
        path: "/create_order_form",
        name: "create_order_form",
        component: () => import(/* webpackChunkName: "create_order_form" */ "@/views/inventory/CreateOrder")
    },
]

const routes = baseRoutes.concat(adminRoutes)

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
    linkActiveClass: "active",
    linkExactActiveClass: "exact-active",
})

router.afterEach((to, from, next) => {
  document.title = to.meta.title || 'Invenotry Management';
  next();
});

export default router
