import {MutationTree} from "vuex";
import {CustomerState} from "~/stores/customer/types";
import {Customer} from "~/models/customer";

export const customerMutations = <MutationTree<CustomerState>>{
    getList(state: CustomerState, customers: Customer[]) {
        state.customers = customers;
    }
    ,
    getOne(state: CustomerState, customer: Customer) {
        state.customer = customer;
    }
}
