import axios from "axios";
import {config} from "@/config/config"
import {Commit} from "vuex";
import {User} from "@/models/user";

const BASE_URL = `${config.BASE_URL}/users`

export interface UserState {
    user: User
    users: User[]
}

const userStore = {
    state() {
        return {}
    },
    namespaced: true,
    actions: {

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
    },
    mutations: {
        GET_ALL(state: UserState, users: User[]) {
            state.users = users
        }
    }
}

export default userStore