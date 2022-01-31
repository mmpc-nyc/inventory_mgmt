import {actions} from "@/stores/equipment/actions";
import {mutations} from "@/stores/equipment/mutations";
import {EquipmentState} from "@/stores/equipment/types";
import {Module} from "vuex";
import {RootState} from "@/stores/types";

export const equipmentStore: Module<EquipmentState, RootState> = {
    state: new EquipmentState(),
    namespaced: true,
    mutations: mutations,
    actions: actions
}

export default equipmentStore