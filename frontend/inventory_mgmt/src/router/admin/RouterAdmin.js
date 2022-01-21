import customerAdminRoutes from "@/router/admin/RouterAdminCustomer";

const children = customerAdminRoutes

const adminRoutes = [{
    path: "/admin",
    name: "admin",
    title: "Admin",
    component: () => import(/* webpackChunkName: "admin" */ "@/views/admin/TheAdmin"),
    children: children
}]



export default adminRoutes