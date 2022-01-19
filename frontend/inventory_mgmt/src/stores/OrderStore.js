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
                response => {commit('getOrderList', response.data)}
            ).catch(() => {return 'Failed to connect to API'})
        }
    },
    mutations: {
        getOrderList(state, orders) {
            state.orders = orders
        }
    }
}

export default orderStore