import axiosInstance from "../services/AxiosInstance"

const instance = axiosInstance()

const customerStore = {
    state() {
        return {}
    },
    namespaced: true,
    actions: {

        getCustomerList({commit}) {
            instance.get('http://localhost:8000/api/customers/').then(
                response => {
                    commit('getCustomerList', response.data)
                }
            ).catch(() => {
                return 'Failed to connect to API'
            })
        }
    },
    mutations: {
        getCustomerList(state, customers) {
            state.customers = customers
        }
    }
}

export default customerStore