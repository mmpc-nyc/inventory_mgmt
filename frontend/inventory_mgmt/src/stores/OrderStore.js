import axiosInstance from "@/services/AxiosInstance"

import {config} from "@/config/config"

const BASE_URL = `${config.BASE_URL}/orders/`

const orderStore = {
    state() {
        return {}
    },
    namespaced: true,
    actions: {

        getOrderList({commit}) {
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
        getOrderList(state, orders) {
            state.orders = orders
        }
    }
}

export default orderStore