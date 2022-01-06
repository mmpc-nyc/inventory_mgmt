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
                    commit('GET_ALL', response.data)
                }
            ).catch(
                () => {
                    return 'Failed to connect to API'
                }
            )
        },
        deleteEquipment(equipment, {commit}) {
            axios.delete(`http://localhost:8000/api/brands/${equipment.id}`)
                .then(() => {
                    commit('DELETE_ONE', equipment)
                })
        }
    },
    mutations: {
        GET_ALL(state, equipments) {
            state.equipments = equipments
        },
        DELETE_ONE(state, equipment) {
            state.equipments = equipments.filter(eq => {
                return eq === equipment
            })
        }
    }
}

export default equipments