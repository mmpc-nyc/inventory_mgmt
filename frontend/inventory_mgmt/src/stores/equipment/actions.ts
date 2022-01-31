import {config} from "@/config/config";
import {ActionTree, Commit} from "vuex";
import AxiosInstance from "axios";
import {Equipment} from "@/models/equipment";
import {EquipmentState} from "@/stores/equipment/types";

export const BASE_URL = `${config.BASE_URL}/equipments/`

export const actions = <ActionTree<EquipmentState, any>>{
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
    checkIn({state, commit}: { state: EquipmentState, commit: Commit }, id: string) {
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