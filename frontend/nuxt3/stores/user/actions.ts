import {config} from "~/config/config";
import {ActionTree, Commit} from "vuex";
import {UserState} from "~/stores/user/types";
import axios from "axios";

export const BASE_URL = `${config.BASE_URL}/users`
export const actions = <ActionTree<UserState, any>>{
    getList({commit}: { commit: Commit }) {
        axios.get(BASE_URL).then(
            response => {
                commit('GET_ALL', response.data)
            }
        ).catch(
            () => {
                return 'Failed to connect to API'
            }
        )
    }
}