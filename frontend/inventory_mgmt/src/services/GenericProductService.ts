import {config} from "@/config/config";
import axiosInstance from "@/services/AxiosInstance";
import {GenericProduct} from "@/models/genericProduct";
import {AxiosResponse} from "axios";
import {plainToClass} from "class-transformer";

const genericProductService = {
    BASE_URL: `${config.BASE_URL}/generic_products/`,
    OBJECT_CLASS: GenericProduct,

    toClass(response: AxiosResponse) : GenericProduct | GenericProduct[]{
        return plainToClass(this.OBJECT_CLASS, response)
    },

    async getList() {
        return await axiosInstance.get(this.BASE_URL)
    },
    async get(id: string | number) {
        return await axiosInstance.get(`${this.BASE_URL}${id}`)
    },

    async create(genericProduct: GenericProduct) {
        return await axiosInstance.post(this.BASE_URL, genericProduct)
    },

    async search(text: string) : Promise<GenericProduct | GenericProduct[]> {
        return this.toClass((await axiosInstance.get(this.BASE_URL, {params: {search: text}})).data)
    }
}

export default genericProductService