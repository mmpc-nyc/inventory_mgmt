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
        // config.headers["Access-Control-Allow-Credentials"] = "true";
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
        if (err.response.status === 401 && !originalConfig._retry) {
          originalConfig._retry = true;

          try {
            const rs = await axiosInstance.post("/jwt/refresh", {
              refreshToken: TokenService.getLocalRefreshToken(),
            });

            const { access } = rs.data;

            store.dispatch("jwt/refresh", access);
            TokenService.updateLocalAccessToken(access);

            return axiosInstance(originalConfig);
          } catch (_error) {
            eventBus.dispatch("logout");
            return Promise.reject(_error);
          }
        }
      }

      return Promise.reject(err);
    }
  );
};

export default setup;
