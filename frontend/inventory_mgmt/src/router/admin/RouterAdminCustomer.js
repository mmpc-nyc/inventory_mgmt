const customerAdminRoutes = [
    {
        path: "customers",
        name: 'admin_customer',
        component: () => import(/* webpackChunkName: "admin_customer_list" */ "@/views/admin/AdminCustomerIndex"),
        children: [
            {
                path: "list",
                name: 'admin_customer_list',
                component: () => import(/* webpackChunkName: "admin_customer_list" */ "@/views/admin/AdminCustomerList"),
            },
            {
                path: 'create',
                name: 'admin_customer_create',
                component: () => import(/* webpackChunkName: "admin_customer_create" */ "@/views/admin/AdminCustomerCreate"),
            }
        ]
    }
]


export default customerAdminRoutes