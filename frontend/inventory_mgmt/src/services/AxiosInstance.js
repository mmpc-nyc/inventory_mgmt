import axios from "axios";
import {config} from "@/config/config"

let axiosInstance = axios.create({
    baseURL: config.BASE_URL,
    headers: {
        "Content-Type": "application/json",
    }
});

export default axiosInstance;
