import instance from "@/services/AxiosInstance";

import {config} from "@/config/config"

const BASE_URL = `${config.BASE_URL}/customers/`

const customerStore = {
        state() {
            return {};
        },
        namespaced: true,
        actions: {
            getList({commit}) {
                instance
                    .get(BASE_URL)
                    .then((response) => {
                        commit("getList", response.data);
                    })
                    .catch(() => {
                        return "Failed to connect to API";
                    });
            },
            getOne({commit}, data) {
                instance
                    .get(`${BASE_URL}${data}`)
                    .then((response) => {
                        commit("getOne", response.data);
                    })
                    .catch(() => {
                        return "Failed to connect to API";
                    });
            },
            create({commit}, data) {
                console.log(commit, data)
                instance
                    .post(BASE_URL, data)
                    .then((response) => {
                        console.log("Created customer", response.data)
                    }).catch(() => {
                    return "Failed to connect to API";
                });
            },
        },
        mutations: {
            getList(state, customers) {
                state.customers = customers;
            }
            ,
            getOne(state, customer) {
                state.customer = customer;
            }
            ,
        }
    }
;

export default customerStore;
