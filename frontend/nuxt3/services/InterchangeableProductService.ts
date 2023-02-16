import {config} from "@/config/config";
import axiosInstance from "~/services/AxiosInstance";
import {InterchangeableProduct} from "~/models/interchangeableProduct";
import {AxiosResponse} from "axios";
import {plainToClass} from "class-transformer";

const interchangeableProductService = {
    BASE_URL: `${config.BASE_URL}/interchangeable_products/`,
    OBJECT_CLASS: InterchangeableProduct,

    toClass(response: AxiosResponse) : InterchangeableProduct | InterchangeableProduct[]{
        return plainToClass(this.OBJECT_CLASS, response)
    },

    async getList() {
        return await axiosInstance.get(this.BASE_URL)
    },
    async get(id: string | number) {
        return await axiosInstance.get(`${this.BASE_URL}${id}`)
    },

    async create(genericProduct: InterchangeableProduct) {
        return await axiosInstance.post(this.BASE_URL, genericProduct)
    },

    async search(text: string) : Promise<InterchangeableProduct | InterchangeableProduct[]> {
        return this.toClass((await axiosInstance.get(this.BASE_URL, {params: {search: text}})).data)
    }
}

export default interchangeableProductService