import {ActionTree, Commit} from "vuex";
import {CustomerState} from "~/stores/customer/types";

import {plainToClass} from "class-transformer";
import {Customer} from "~/models/customer";
import customerService from "~/services/CustomerService";

export const customerActions = <ActionTree<CustomerState, any>>{
    getList({commit}: { commit: Commit }) {
        customerService.getList()
            .then((response) => {
                commit("getList", response.data);
            })
    },
    getOne({commit}: { commit: Commit }, id: string) {
        customerService.get(id)
            .then((response) => {
                commit("getOne", plainToClass(Customer, response.data));
            })
    },
    create({commit}: { commit: Commit }, customer: Customer) {
        customerService.create(customer)
            .then((response) => {
                console.log("Created customer", response.data)
            })
    }
}