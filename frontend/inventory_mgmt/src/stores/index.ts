import {createStore, Store} from 'vuex'

import {RootState} from "@/stores/types";
import {modules} from "@/stores/modules";

export const store = createStore<RootState>({
    modules: modules
})