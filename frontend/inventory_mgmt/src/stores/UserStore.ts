import axios from "axios";
import {config} from "@/config/config"
import {ActionTree, Commit, MutationTree} from "vuex";
import {AuthUser} from "@/models/authUser";

const BASE_URL = `${config.BASE_URL}/users`

class State {
    user: AuthUser | null = null
    users: AuthUser[] = []
}

const mutations = <MutationTree<State>>{
    getList(state: State, users: AuthUser[]) {
        //TODO Fix This - Replace AuthUser with User
        state.users = users
    }
}

const actions = <ActionTree<State, any>>{
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

const userStore = {
    state: new State(),
    namespaced: true,
    actions: actions,
    mutations: mutations
}

export default userStore