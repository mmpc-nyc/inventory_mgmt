import axiosInstance from "@/services/AxiosInstance"

import {config} from "@/config/config"
import {Commit} from "vuex";
import {Order} from "@/models/order";

const BASE_URL = `${config.BASE_URL}/orders/`

export interface OrderState{
    order: Order
    orders: Order[]
}

const orderStore = {
    state() {
        return {}
    },
    namespaced: true,
    actions: {

        getOrderList({commit}: { commit: Commit }) {
            axiosInstance.get(BASE_URL).then(
                response => {
                    commit('getOrderList', response.data)
                }
            ).catch(() => {
                return 'Failed to connect to API'
            })
        }
    },
    mutations: {
        getOrderList(state: OrderState, orders: Order[]) {
            state.orders = orders
        }
    }
}

export default orderStore