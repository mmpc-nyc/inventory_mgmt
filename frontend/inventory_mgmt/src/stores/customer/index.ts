import {Module} from "vuex"
import {RootState} from "@/stores/types";
import {CustomerState} from "@/stores/customer/types";
import {customerActions} from "@/stores/customer/actions";
import {customerMutations} from "@/stores/customer/mutations";


export const customerStore: Module<CustomerState, RootState> = {
        state: new CustomerState(),
        namespaced: true,
        actions: customerActions,
        mutations: customerMutations
    }
;

export default customerStore;
