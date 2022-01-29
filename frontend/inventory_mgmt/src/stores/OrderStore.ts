import axiosInstance from "@/services/AxiosInstance"

import {config} from "@/config/config"
import {ActionTree, Commit, mapMutations, MutationTree} from "vuex";
import {Order} from "@/models/order";

const BASE_URL = `${config.BASE_URL}/orders/`

class State {
    order: Order | null = null
    orders: Order[] = []
}

const actions = <ActionTree<State, any>>{

    getOrderList({commit}: { commit: Commit }) {
        axiosInstance.get(BASE_URL).then(
            response => {
                commit('getOrderList', response.data)
            }
        ).catch(() => {
            return 'Failed to connect to API'
        })
    }
}

const mutations = <MutationTree<State>>{
    getOrderList(state: State, orders: Order[]) {
        state.orders = orders
    }
}


const orderStore = {
    state() {
        return {}
    },
    namespaced: true,
    actions: actions,
    mutations: mutations
}

export default orderStore