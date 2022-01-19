import axios from "axios";
import authHeader from "../services/AuthHeader"
const orderStore = {
    state() {
        return {}
    },
    namespaced: true,
    actions: {

        getOrderList({commit}) {
            console.log('what the fuck')
            axios.get(
                'http://localhost:8000/api/orders/',
                {headers: authHeader()}
            ).then(
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
        GET_ALL(state, orders) {
            state.orders = orders
        }
    }
}

export default orderStore