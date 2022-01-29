import {config} from "@/config/config"
import {ActionTree, Commit, MutationTree} from "vuex";
import {Equipment} from "@/models/equipment";
import AxiosInstance from "axios";

const BASE_URL = `${config.BASE_URL}/equipments/`

class State {
    equipment: Equipment | null = null
    equipments: Equipment[] = []
}

const mutations = <MutationTree<State>>{
    getList(state: State, equipments: Equipment[]) {
        state.equipments = equipments
    },
    get(state: State, equipment: Equipment) {
        state.equipment = equipment
    },
    delete(state: State, equipment: Equipment) {
        console.log('Delete Equipment', state, equipment)
        // TODO Implement Delete Equipment Function
    },
    checkIn(state: State, equipment: Equipment) {
        console.log('Check In Equipment', state, equipment)
        // TODO Implement Check In Equipment Function
    },

};

const actions = <ActionTree<State, any>>{
    getList({commit}: { commit: Commit }) {
        AxiosInstance.get(BASE_URL).then(
            response => {
                commit('getList', response.data)
            }
        ).catch(
            (response) => {
                return response
            }
        )
    },
    get({commit}: { commit: Commit }, id: string) {
        AxiosInstance.get(`${BASE_URL}/${id}`).then(
            response => {
                commit('get', response.data)
            }
        ).catch(
            (response) => {
                return response
            }
        )
    },
    checkIn({state, commit}: { state: State, commit: Commit }, id: string) {
        if (state.equipments) {
            // TODO Implement this function
            return
        }
        AxiosInstance.get(`${BASE_URL}/${id}`).then(
            response => {
                commit('checkIn', response.data)
            }
        ).catch(
            (response) => {
                return response
            }
        )
    },
    deleteEquipment({commit}: { commit: Commit }, equipment: Equipment) {
        AxiosInstance.delete(`http://localhost:8000/api/equipments/${equipment.id}`)
            .then(response => {
                commit('delete', equipment)
            })
    }
}

const equipmentStore = {
    state: new State(),
    namespaced: true,
    mutations: mutations,
    actions: actions
}

export default equipmentStore