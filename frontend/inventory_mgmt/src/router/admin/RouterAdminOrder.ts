export const orderAdminRoutes = [
    {
        path: "list",
        name: 'admin_order_list',
        meta: {
            auth: true,
            title: 'Orders',
        },
        component: () => import(/* webpackChunkName: "admin_order_list" */ "@/views/admin/AdminOrderListView.vue"),
    },
    {
        path: 'create',
        name: 'admin_order_create',
        meta: {
            auth: true,
            title: 'Add Order',
        },
        component: () => import(/* webpackChunkName: "admin_order_create" */ "@/views/admin/AdminOrderCreateView.vue"),
    },
    {
        path: ':id',
        name: 'admin_order_detail',
        meta: {
            auth: true,
            title: 'Order Detail',
        },
        component: () => import(/* webpackChunkName: "admin_order_detail" */ "@/views/admin/AdminOrderDetailView.vue")
    }
]
export default orderAdminRoutes