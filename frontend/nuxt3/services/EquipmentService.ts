import {config} from "@/config/config";
import axiosInstance from "~/services/AxiosInstance";
import {Equipment} from "@/models/equipment";
import {AxiosResponse} from "axios";
import {plainToClass} from "class-transformer";

const equipmentService = {
    BASE_URL: `${config.BASE_URL}/equipments/`,
    OBJECT_CLASS: Equipment,

    toClass(response: AxiosResponse) : Equipment | Equipment[]{
        return plainToClass(this.OBJECT_CLASS, response)
    },

    async getList() {
        return await axiosInstance.get(this.BASE_URL)
    },
    async get(id: string | number) {
        return await axiosInstance.get(`${this.BASE_URL}${id}`)
    },

    async create(equipment: Equipment) {
        return await axiosInstance.post(this.BASE_URL, equipment)
    },

    async search(text: string) : Promise<Equipment | Equipment[]> {
        return this.toClass((await axiosInstance.get(this.BASE_URL, {params: {search: text}})).data)
    }
}

export default equipmentService