import axiosInstance from "@/services/AxiosInstance";
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
            const originalConfig = error.config;
            try {
                const accessToken = await authService.refresh()

                if (accessToken) {
                    await store.dispatch("auth/setAccessToken", accessToken);
                    return axiosInstance(originalConfig);
                }
            } catch (error) {
                await store.dispatch("auth/logout")
                return Promise.reject(error)
            }
        }
    );
};

export default setup;
