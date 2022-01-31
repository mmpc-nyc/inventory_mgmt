const customerAdminRoutes = [
    {
        path: "customers",
        name: 'admin_customer',
        meta: {
            auth: true,
            title: 'Customer Admin',
        },
        component: () => import(/* webpackChunkName: "admin_customer_list" */ "@/views/admin/AdminCustomerIndexView.vue"),
        children: [
            {
                path: "list",
                name: 'admin_customer_list',
                meta: {
                    auth: true,
                    title: 'Customers',
                },
                component: () => import(/* webpackChunkName: "admin_customer_list" */ "@/views/admin/AdminCustomerListView.vue"),
            },
            {
                path: 'create',
                name: 'admin_customer_create',
                meta: {
                    auth: true,
                    title: 'Add Customer',
                },
                component: () => import(/* webpackChunkName: "admin_customer_create" */ "@/views/admin/AdminCustomerCreateView.vue"),
            },
            {
                path: ':id',
                name: 'admin_customer_detail',
                meta: {
                    auth: true,
                    title: 'Customer Detail',
                },
                component: () => import(/* webpackChunkName: "admin_customer_detail" */ "@/views/admin/AdminCustomerDetailView.vue")
            }
        ]
    }
]

export default customerAdminRoutes