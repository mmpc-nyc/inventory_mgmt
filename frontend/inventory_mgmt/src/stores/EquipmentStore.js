import axios from "axios";


const BASE_URL = 'http://localhost:8000/api/equipments'
const instance = axios.create({
    timeout: 1000,
    headers: {'Content-Type': 'application/json'}
})

const equipmentStore = {
    state() {
        return {
            equipments: new Map,
            equipment: null,
        }

    },
    namespaced: true,
    actions: {

        getList({commit}) {
            instance.get('http://localhost:8000/api/equipments/').then(
                response => {
                    commit('getList', response.data)
                }
            ).catch(
                (response) => {
                    return response
                }
            )
        },
        get({commit}, equipmentId) {
            instance.get(`${BASE_URL}/${equipmentId}`).then(
                response => {
                    commit('get', response.data)
                }
            ).catch(
                (response) => {
                    return response
                }
            )
        },
        checkIn({state, commit}, equipmentId) {
            if (state.equipments.has(equipmentId)) {
                return
            }
            instance.get(`${BASE_URL}/${equipmentId}`).then(
                response => {
                    commit('checkIn', response.data)
                }
            ).catch(
                (response) => {
                    return response
                }
            )


        },
        deleteEquipment(equipment, {commit}) {
            instance.delete(`http://localhost:8000/api/equipments/${equipment.id}`)
                .then(() => {
                    commit('delete', equipment)
                })
        }
    },
    mutations: {
        getList(state, equipments) {
            state.equipments = equipments
        },
        get(state, equipment) {
            state.equipment = equipment
        },
        delete(state, equipment) {
            state.equipments.delete(equipment.id)
        },
        checkIn(state, equipment) {
            console.log(state.equipments)
            state.equipments.set(equipment.id, equipment)
        },

    }
}

export default equipmentStore