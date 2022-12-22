import {MutationTree} from "vuex";
import {UserState} from "~/stores/user/types";
import {AuthUser} from "~/models/authUser";

export const mutations = <MutationTree<UserState>>{
    getList(state: UserState, users: AuthUser[]) {
        //TODO Fix This - Replace AuthUser with User
        state.users = users
    }
}