import axios from "axios";

const equipments = {
    state() {
        return {}
    },
    namespaced: true,
    actions: {

        getList({commit}) {
            axios.get('http://localhost:8000/api/equipments/').then(
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
        GET_ALL(state, equipments) {
            state.equipments = equipments
        }
    }
}

export default equipments