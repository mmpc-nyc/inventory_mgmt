import {createApp} from 'vue'
import App from './App.vue'

import BalmUI from 'balm-ui'
import 'balm-ui-css';

import router from './router/Router'
import {store} from "./stores/Store";

const app = createApp(App)
app.use(router)
app.use(BalmUI)
app.use(store)
app.mount('#app')
