import eventBus from "../common/EventBus";
import TokenService from "./TokenService";
import axiosInstance from "./AxiosInstance";

const setup = (store) => {
  axiosInstance.interceptors.request.use(
    (config) => {
      const token = TokenService.getLocalAccessToken();
      if (token) {
        // config.headers["Authorization"] = 'Bearer ' + token;  // for Spring Boot back-end
        // config.headers["x-access-token"] = token; // for Node.js Express back-end
        config.headers["Authorization"] = "JWT " + token; // for Spring Boot back-end
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
    async (err) => {
      const originalConfig = err.config;

      if (originalConfig.url !== "/auth/signin" && err.response) {
        // Access Token was expired
        console.log(err.response.status, originalConfig._retry);
        if (err.response.status === 401 && !originalConfig._retry) {
          originalConfig._retry = true;

          try {
            const rs = await axiosInstance.post("/auth/jwt/refresh", {
              refresh: TokenService.getLocalRefreshToken(),
            });

            const { access } = rs.data;

            store.dispatch("auth/refreshToken", access);
            TokenService.updateLocalAccessToken(access);

            return axiosInstance(originalConfig);
          } catch (_error) {
            eventBus.dispatch("logout");
            return Promise.reject(_error);
          }
        }
      }

      eventBus.dispatch("logout");
      return Promise.reject(err);
    }
  );
};

export default setup;
