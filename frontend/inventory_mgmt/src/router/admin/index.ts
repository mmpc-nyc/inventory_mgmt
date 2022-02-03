import customerAdminRoutes from "@/router/admin/RouterAdminCustomer";
import orderAdminRoutes from "@/router/admin/RouterAdminOrder";

const adminRoutes = [{
    path: "/admin",
    name: "admin",
    meta: {
        auth: true,
        title: 'Admin',
    },
    component: () => import(/* webpackChunkName: "admin" */ "@/views/admin/TheAdmin.vue"),
    children: [
        {
            path: "customers",
            name: 'admin_customer',
            meta: {
                auth: true,
                title: 'Customer Admin',
            },
            component: () => import(/* webpackChunkName: "admin_customer_list" */ "@/views/admin/AdminCustomerIndexView.vue"),
            children: customerAdminRoutes
        },
        {
            path: "orders",
            name: 'admin_order',
            meta: {
                auth: true,
                title: 'Order Admin',
            },
            component: () => import(/* webpackChunkName: "admin_order_list" */ "@/views/admin/AdminOrderIndexView.vue"),
            children: orderAdminRoutes
        }]
}]


export default adminRoutes