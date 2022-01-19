import {createStore} from 'vuex'
import equipmentStore from "@/stores/EquipmentStore";
import userStore from "@/stores/UserStore";
import orderStore from "@/stores/OrderStore";
import authStore from "@/stores/AuthStore"

export const store = createStore({
    state() {
        return {}
    },
    modules: {
        auth: authStore,
        equipments: equipmentStore,
        users: userStore,
        orders: orderStore
    }
})