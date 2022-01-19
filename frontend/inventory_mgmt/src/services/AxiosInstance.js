import axios from 'axios'
import authHeader from "./AuthHeader";

export default function axiosInstance() {
    return axios.create({
        baseURL: 'http://localhost:8000',
        headers: authHeader()
    })
}