import axiosInstance from "@/services/AxiosInstance";
import {Store} from "vuex";
import AuthService from "@/services/AuthService";
import authService from "@/services/AuthService";

const setup = (store: Store<any>) => {
    axiosInstance.interceptors.request.use(
        (config) => {
            const token = AuthService.getAccessToken();
            if (token) {
                config.headers!["Authorization"] = "JWT " + token;
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
            const authUser = authService.AuthStorage.getAuthUser()
            console.log(
                authUser , authUser.loggedIn ,
                authUser.refresh ,
                typeof originalConfig._retry === 'undefined' ,
                !originalConfig._retry)
            if (
                authUser && authUser.loggedIn &&
                authUser.refresh &&
                typeof originalConfig._retry !== 'undefined' &&
                !originalConfig._retry
            ) {
                originalConfig._retry = true
                const accessToken = await authService.refresh().then(
                    function resolve(accessToken) {
                        return Promise.resolve(accessToken)
                    }
                )
                console.log(accessToken)
                if (accessToken) {
                    console.log(accessToken)
                    await store.dispatch("auth/setAccessToken", accessToken);
                    return axiosInstance(originalConfig);
                }
            }
            await store.dispatch("auth/logout")
            return Promise.reject(error)
        }
    );
};

export default setup;
