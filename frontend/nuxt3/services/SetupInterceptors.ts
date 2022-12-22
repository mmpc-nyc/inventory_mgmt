import axiosInstance from "~/services/AxiosInstance";
import {Store} from "vuex";
import AuthService from "@/services/AuthService";
import authService from "@/services/AuthService";

const setup = (store: Store<any>) => {
    axiosInstance.interceptors.request.use(
        (config) => {
            const accessToken = AuthService.getAccessToken();
            if (accessToken) {
                config.headers!["Authorization"] = "JWT " + accessToken;
            }
            return config;
        },
        (error) => {
            return Promise.reject(error);
        }
    );

    axiosInstance.interceptors.response.use(
        (res) => {
            return res;
        },
        async (error) => {
            try {
                await store.dispatch("auth/setAccessToken", await authService.refresh());
                return axiosInstance(error.config);
            } catch (error) {
                await store.dispatch("auth/logout")
                return Promise.reject(error)
            }
        }
    );
};

export default setup;
