import {MutationTree} from "vuex";
import {OrderState} from "@/stores/order/types";
import {Order} from "@/models/order";

export const mutations = <MutationTree<OrderState>>{
    getOrderList(state: OrderState, orders: Order[]) {
        state.orders = orders
    }
}