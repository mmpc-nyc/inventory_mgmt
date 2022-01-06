import axios from "axios";

const users = {
    state() {
        return {}
    },
    namespaced: true,
    actions: {

        getList({commit}) {
            axios.get('http://localhost:8000/api/users/').then(
                response => {
                    console.log('axios')
                    console.log(response.data)
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

export default users