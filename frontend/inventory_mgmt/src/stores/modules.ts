import {ModuleTree} from "vuex";
import {RootState} from "@/stores/types";
import authStore from "@/stores/auth"
import customerStore from "@/stores/customer";
import equipmentStore from "@/stores/equipment"
import orderStore from "@/stores/order"
import userStore from "@/stores/user"

export const modules: ModuleTree<RootState> = {
        auth: authStore,
        equipments: equipmentStore,
        users: userStore,
        orders: orderStore,
        customers: customerStore

}