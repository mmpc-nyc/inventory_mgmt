import {createRouter, createWebHistory} from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/my_equipment',
        name: 'my_equipment',
        component: () => import(/* webpackChunkName: "my_equipment" */ '../views/MyEquipment.vue')
    },
    {
        path: '/my_orders',
        name: 'my_orders',
        component: () => import(/* webpackChunkName: "my_orders" */ '../views/MyOrders.vue')
    },
    {
        path: '/equipment_checkin',
        name: 'equipment_checkin',
        component: () => import(/* webpackChunkName: "equipment_checkin" */ '../views/EquipmentCheckin')
    },
    {
        path: '/create_order_form',
        name: 'create_order_form',
        component: () => import(/* webpackChunkName: "create_order_form" */ '../views/CreateOrderForm')
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
