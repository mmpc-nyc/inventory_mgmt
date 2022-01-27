const customerAdminRoutes = [
    {
        path: "customers",
        name: 'admin_customer',
        component: () => import(/* webpackChunkName: "admin_customer_list" */ "@/views/admin/AdminCustomerIndex"),
        children: [
            {
                path: "list",
                name: 'admin_customer_list',
                component: () => import(/* webpackChunkName: "admin_customer_list" */ "@/views/admin/AdminCustomers"),
            },
            {
                path: 'create',
                name: 'admin_customer_create',
                component: () => import(/* webpackChunkName: "admin_customer_create" */ "@/views/admin/AdminCustomerCreate"),
            },
            {
                path: ':id',
                name: 'admin_customer_detail',
                component: () => import(/* webpackChunkName: "admin_customer_detail" */ "@/views/admin/AdminCustomerDetail")
            }
        ]
    }
]


export default customerAdminRoutes