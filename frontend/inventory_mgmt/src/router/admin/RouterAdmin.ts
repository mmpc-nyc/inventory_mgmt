import customerAdminRoutes from "@/router/admin/RouterAdminCustomer";
import orderAdminRoutes from "@/router/admin/RouterAdminOrder";
import RouteConfig from "@/router/types";

const children: RouteConfig[] = []
children.concat(customerAdminRoutes)
children.concat(orderAdminRoutes)

const adminRoutes = [{
    path: "/admin",
    name: "admin",
    meta: {
        auth: true,
        title: 'Admin',
    },
    component: () => import(/* webpackChunkName: "admin" */ "@/views/admin/TheAdmin.vue"),
    children: children
}]


export default adminRoutes