import instance from "../services/AxiosInstance";

const customerStore = {
        state() {
            return {};
        },
        namespaced: true,
        actions: {
            getCustomerList({commit}) {
                instance
                    .get("http://localhost:8000/api/customers/")
                    .then((response) => {
                        commit("getCustomerList", response.data);
                    })
                    .catch(() => {
                        return "Failed to connect to API";
                    });
            },
            create({commit}, data) {
                console.log(commit, data)
                instance
                    .post('http://localhost:8000/api/customers/', data)
                    .then((response) => {
                        console.log("Created customer", response.data)
                    }).catch(() => {
                    return "Failed to connect to API";
                });
            }
        },
        mutations: {
            getCustomerList(state, customers) {
                state.customers = customers;
            }
            ,
        }
        ,
    }
;

export default customerStore;
