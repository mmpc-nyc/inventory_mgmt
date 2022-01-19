import axiosInstance from "./AxiosInstance";

const setup = (store) => {
  axiosInstance.interceptors.request.use();
};
