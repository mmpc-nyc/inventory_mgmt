import {createStore} from 'vuex'
import equipments from "@/stores/equipments";
import users from "@/stores/users";

export const store = createStore({
    state() {
        return {}
    },
    modules: {
        equipments: equipments,
        users: users
    }
})