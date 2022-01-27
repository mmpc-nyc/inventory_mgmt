import axios from "axios";
import {config} from "@/config/config"

const BASE_URL = `${config.BASE_URL}/users`

const userStore = {
    state() {
        return {}
    },
    namespaced: true,
    actions: {

        getList({commit}) {
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
    },
    mutations: {
        GET_ALL(state, users) {
            state.users = users
        }
    }
}

export default userStore