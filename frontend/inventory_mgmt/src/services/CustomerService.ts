import {config} from "@/config/config";
import axiosInstance from "@/services/AxiosInstance";
import {Customer} from "@/models/customer";
import {AxiosResponse} from "axios";
import {plainToClass} from "class-transformer";

const customerService = {
    BASE_URL: `${config.BASE_URL}/customers/`,
    OBJECT_CLASS: Customer,

    toClass(response: AxiosResponse) : Customer | Customer[]{
        return plainToClass(this.OBJECT_CLASS, response)
    },

    async getList() {
        return await axiosInstance.get(this.BASE_URL)
    },
    async get(id: string | number) {
        return await axiosInstance.get(`${this.BASE_URL}${id}`)
    },

    async create(customer: Customer) {
        return await axiosInstance.post(this.BASE_URL, customer)
    },

    async search(text: string) {
        return await axiosInstance.get(this.BASE_URL, {params: {search: text}})
    }
}

export default customerService