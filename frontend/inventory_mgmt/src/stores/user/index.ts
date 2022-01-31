import {actions} from "@/stores/user/actions";
import {UserState} from "@/stores/user/types";
import {mutations} from "@/stores/user/mutations";
import {Module} from "vuex";
import {RootState} from "@/stores/types";

export const userStore : Module<UserState, RootState> ={
    state: new UserState(),
    namespaced: true,
    actions: actions,
    mutations: mutations
}

export default userStore