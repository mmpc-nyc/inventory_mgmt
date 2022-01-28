import {createApp} from "vue";
import App from "@/App.vue";

import BalmUI from "balm-ui";
import "balm-ui-css";
import VueGoogleMaps from '@fawmi/vue-google-maps'
import router from "@/router/Router";
import {store} from "@/stores/Store";
import setupInterceptors from "@/services/SetupInterceptors";
import {config} from "@/config/config.js";
import validatorRules from "@/config/validator-rules";

setupInterceptors(store)

const app = createApp(App);
app.use(router);
app.use(BalmUI, {
    $validator: validatorRules
});
app.use(store);
app.config.globalProperties.$config = config
app.use(VueGoogleMaps, {
    load: {
        key: process.env.VUE_APP_GOOGLE_API_KEY,
        libraries: "places"
    }
})
app.mount("#app");
