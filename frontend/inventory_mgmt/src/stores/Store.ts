import {createStore, Store} from 'vuex'
import equipmentStore from "@/stores/EquipmentStore";
import userStore from "@/stores/UserStore";
import orderStore from "@/stores/OrderStore";
import authStore from "@/stores/AuthStore"
import customerStore from "@/stores/CustomerStore";
import {InjectionKey} from "vue";

export interface State {}

export const key: InjectionKey<Store<State>> = Symbol()

export const store = createStore<State>({
    state() {
        return {}
    },
    modules: {
        auth: authStore,
        equipments: equipmentStore,
        users: userStore,
        orders: orderStore,
        customers: customerStore
    }
})