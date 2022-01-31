import {config} from "@/config/config";
import {ActionTree, Commit} from "vuex";
import {OrderState} from "@/stores/order/types";
import axiosInstance from "@/services/AxiosInstance";

export const BASE_URL = `${config.BASE_URL}/orders/`
export const actions = <ActionTree<OrderState, any>>{

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