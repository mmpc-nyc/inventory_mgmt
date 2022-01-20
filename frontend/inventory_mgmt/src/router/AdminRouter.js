import CustomerAdmin from '@/views/admin/CustomerAdmin'
const adminRoutes = [{
    path: "/admin",
    name: "admin",
    title: "Admin",
    component: () => import(/* webpackChunkName: "admin" */ "../views/admin/TheAdmin"),
    children: [
        {
            path: 'customers',
            name: 'customers_admin',
            component: CustomerAdmin

        }
    ]
}]


export default adminRoutes