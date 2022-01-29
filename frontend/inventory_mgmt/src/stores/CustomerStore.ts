import instance from "@/services/AxiosInstance";

import {config} from "@/config/config"
import {Customer} from "@/models/customer";
import {Commit} from "vuex"

const BASE_URL = `${config.BASE_URL}/customers/`

export interface CustomerState {
    customer: Customer
    customers: Customer[]
}


const customerStore = {
        state() {
            return {};
        },
        namespaced: true,
        actions: {
            getList({commit}: { commit: Commit }) {
                instance
                    .get(BASE_URL)
                    .then((response) => {
                        commit("getList", response.data);
                    })
                    .catch(() => {
                        return "Failed to connect to API";
                    });
            },
            getOne({commit}: { commit: Commit }, id: string) {
                instance
                    .get(`${BASE_URL}${id}`)
                    .then((response) => {
                        commit("getOne", response.data);
                    })
                    .catch(() => {
                        return "Failed to connect to API";
                    });
            },
            create({commit}: { commit: Commit }, customer: Customer) {
                instance
                    .post(BASE_URL, customer)
                    .then((response) => {
                        console.log("Created customer", response.data)
                    }).catch(() => {
                    return "Failed to connect to API";
                });
            },
        },
        mutations: {
            getList(state: CustomerState, customers: Customer[]) {
                state.customers = customers;
            }
            ,
            getOne(state: CustomerState, customer: Customer) {
                state.customer = customer;
            }
            ,
        }
    }
;

export default customerStore;
