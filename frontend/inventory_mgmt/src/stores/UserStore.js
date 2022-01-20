import axios from "axios";

const userStore = {
    state() {
        return {}
    },
    namespaced: true,
    actions: {

        getList({commit}) {
            axios.get('http://localhost:8000/api/users/').then(
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