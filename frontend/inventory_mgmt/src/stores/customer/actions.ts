import {ActionTree, Commit} from "vuex";
import {CustomerState} from "@/stores/customer/types";
import instance from "@/services/AxiosInstance";
import {plainToClass} from "class-transformer";
import {Customer} from "@/models/customer";
import {config} from "@/config/config";

const BASE_URL = `${config.BASE_URL}/customers/`

export const customerActions = <ActionTree<CustomerState, any>>{
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
                commit("getOne", plainToClass(Customer, response.data));
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
    }
}