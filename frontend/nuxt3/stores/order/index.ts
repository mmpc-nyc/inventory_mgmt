import {actions} from "~/stores/order/actions";
import {mutations} from "~/stores/order/mutations";
import {Module} from "vuex";
import {RootState} from "~/stores/types";
import {OrderState} from "~/stores/order/types";


export const orderStore : Module<OrderState, RootState> ={
    state: new OrderState(),
    namespaced: true,
    actions: actions,
    mutations: mutations
}

export default orderStore