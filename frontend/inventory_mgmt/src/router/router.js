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
        path: '/equipment_checkin',
        name: 'equipment_checkin',
        component: () => import(/* webpackChunkName: "equipment_checkin" */ '../views/EquipmentCheckin')
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router