import axios from "axios";

const orderStore = {
    state() {
        return {}
    },
    namespaced: true,
    actions: {

        getOrderList({commit}) {
            axios.get('http://localhost:8000/api/orders/').then(
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
        GET_ALL(state, orders) {
            state.orders = orders
        }
    }
}

export default orderStore