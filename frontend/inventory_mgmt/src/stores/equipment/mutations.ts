import {MutationTree} from "vuex";
import {Equipment} from "@/models/equipment";
import {EquipmentState} from "@/stores/equipment/types";

export const mutations = <MutationTree<EquipmentState>>{
    getList(state: EquipmentState, equipments: Equipment[]) {
        state.equipments = equipments
    },
    get(state: EquipmentState, equipment: Equipment) {
        state.equipment = equipment
    },
    delete(state: EquipmentState, equipment: Equipment) {
        console.log('Delete Equipment', state, equipment)
        // TODO Implement Delete Equipment Function
    },
    checkIn(state: EquipmentState, equipment: Equipment) {
        console.log('Check In Equipment', state, equipment)
        // TODO Implement Check In Equipment Function
    },

};