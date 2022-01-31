import {AuthState} from "@/stores/auth/types";
import {mutations} from "@/stores/auth/mutations";
import {actions} from "@/stores/auth/actions";

const index = {
    namespaced: true,
    state: new AuthState(),
    actions: actions,
    mutations: mutations,
};

export default index;
