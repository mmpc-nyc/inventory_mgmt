import {createStore} from 'vuex'
import equipmentStore from "@/stores/EquipmentStore";
import userStore from "@/stores/UserStore";
import orderStore from "@/stores/OrderStore";

export const store = createStore({
    state() {
        return {}
    },
    modules: {
        equipments: equipmentStore,
        users: userStore,
        orders: orderStore
    }
})