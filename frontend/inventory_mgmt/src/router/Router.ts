import {createRouter, createWebHistory} from "vue-router"
import adminRoutes from "@/router/admin/RouterAdmin";
import {store} from "@/stores";

const baseRoutes = [
    {
        path: "/",
        name: "home",
        meta: {
            auth: false,
            title: 'Home',
        },
        component: () => import(/* webpackChunkName: "home" */ "@/views/admin/TheAdmin.vue"),
    },
    {
        path: "/my_equipment",
        name: "my_equipment",
        meta: {
            auth: true,
            title: 'My Equipment',
        },
        component: () => import(/* webpackChunkName: "my_equipment" */ "@/views/inventory/MyEquipment.vue")
    },
    {
        path: "/my_orders",
        name: "my_orders",

        meta: {
            auth: true,
            title: 'My Orders',
        },
        component: () => import(/* webpackChunkName: "my_orders" */ "@/views/inventory/MyOrders.vue")
    },
    {
        path: "/equipment_collect",
        name: "equipment_collect",

        meta: {
            auth: true,
            title: 'Collect Equipment',
        },
        component: () => import(/* webpackChunkName: "equipment_collect" */ "@/views/inventory/EquipmentCollect.vue")
    },
    {
        path: "/create_order_form",
        name: "create_order_form",
        meta: {
            auth: true,
            title: 'Create Order',
        },
        component: () => import(/* webpackChunkName: "create_order_form" */ "@/views/inventory/CreateOrder.vue")
    },
]

const routes = baseRoutes.concat(adminRoutes)

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
    linkActiveClass: "active",
    linkExactActiveClass: "exact-active",
})

router.beforeEach((to, from, next) => {

    if (to.meta.auth && !store.state.auth.authUser.loggedIn) {
        next({name: 'home'})
    }
    else {
        next()
    }
});

router.afterEach((to, from, next) => {
    document.title = typeof (to.meta.title) === "string" ? to.meta.title : 'Inventory Management';
});

export default router
