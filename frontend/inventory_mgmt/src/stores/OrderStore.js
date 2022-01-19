import axiosInstance from "../services/AxiosInstance"

const instance = axiosInstance()

const orderStore = {
    state() {
        return {}
    },
    namespaced: true,
    actions: {

        getOrderList({commit}) {
            instance.get('http://localhost:8000/api/orders/').then(
                response => {commit('GET_ALL', response.data)}
            ).catch(() => {return 'Failed to connect to API'})
        }
    },
    mutations: {
        GET_ALL(state, orders) {
            state.orders = orders
        }
    }
}

export default orderStore