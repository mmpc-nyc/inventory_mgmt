const customerAdminRoutes = [
    {
        path: "customers",
        name: 'admin_customer',
        meta: {
            auth: true,
            title: 'Customer Admin',
        },
        component: () => import(/* webpackChunkName: "admin_customer_list" */ "@/views/admin/AdminCustomerIndex"),
        children: [
            {
                path: "list",
                name: 'admin_customer_list',
                meta: {
                    auth: true,
                    title: 'Customer',
                },
                component: () => import(/* webpackChunkName: "admin_customer_list" */ "@/views/admin/AdminCustomers"),
            },
            {
                path: 'create',
                name: 'admin_customer_create',
                meta: {
                    auth: true,
                    title: 'Add Customer',
                },
                component: () => import(/* webpackChunkName: "admin_customer_create" */ "@/views/admin/AdminCustomerCreate"),
            },
            {
                path: ':id',
                name: 'admin_customer_detail',
                meta: {
                    auth: true,
                    title: 'Customer Detail',
                },
                component: () => import(/* webpackChunkName: "admin_customer_detail" */ "@/views/admin/AdminCustomerDetail")
            }
        ]
    }
]


export default customerAdminRoutes