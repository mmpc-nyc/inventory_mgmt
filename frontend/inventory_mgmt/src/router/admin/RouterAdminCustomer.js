import CustomerAdminCreate from '@/views/admin/customer/CustomerAdminCreate'

const customerAdminRoutes = [{
    path: "/customer",
    name: "customer_admin",
    title: "customer_admin",
    component: () => import(/* webpackChunkName: "admin" */ "@/views/admin/customer/CustomerAdmin"),
    children: [
        {
            path: 'customer_admin_create',
            name: 'customer_admin_create',
            component: CustomerAdminCreate

        }
    ]
}]


export default customerAdminRoutes