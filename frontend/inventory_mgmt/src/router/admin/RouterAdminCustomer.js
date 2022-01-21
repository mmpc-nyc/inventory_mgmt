const customerAdminRoutes = [{
    path: "customers",
    name: "admin_customer_list",
    title: "admin_customer_list",
    component: () => import(/* webpackChunkName: "admin_customer_list" */ "@/views/admin/AdminCustomerList"),
    children: [
        {
            path: 'create',
            name: 'admin_customer_create',
            component: () => import(/* webpackChunkName: "admin_customer_create" */ "@/views/admin/AdminCustomerCreate"),

        }
    ]
}]


export default customerAdminRoutes