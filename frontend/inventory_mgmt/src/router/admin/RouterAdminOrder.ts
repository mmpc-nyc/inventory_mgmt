const orderAdminRoutes = [
    {
        path: "orders",
        name: 'admin_order',
        meta: {
            auth: true,
            title: 'Customer Admin',
        },
        component: () => import(/* webpackChunkName: "admin_order_list" */ "@/views/admin/AdminCustomerIndexView.vue"),
        children: [
            {
                path: "list",
                name: 'admin_order_list',
                meta: {
                    auth: true,
                    title: 'Customers',
                },
                component: () => import(/* webpackChunkName: "admin_order_list" */ "@/views/admin/AdminCustomerListView.vue"),
            },
            {
                path: 'create',
                name: 'admin_order_create',
                meta: {
                    auth: true,
                    title: 'Add Customer',
                },
                component: () => import(/* webpackChunkName: "admin_order_create" */ "@/views/admin/AdminCustomerCreateView.vue"),
            },
            {
                path: ':id',
                name: 'admin_order_detail',
                meta: {
                    auth: true,
                    title: 'Customer Detail',
                },
                component: () => import(/* webpackChunkName: "admin_order_detail" */ "@/views/admin/AdminCustomerDetailView.vue")
            }
        ]
    }
]

export default orderAdminRoutes