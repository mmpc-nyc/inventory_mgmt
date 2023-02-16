import {InterchangeableProduct} from "./interchangeableProduct";

export class Brand{
    id?: number
}

export type ProductStatus = "Active" | "Inactive" | "Recall"

export class Product{
    id?: number
    interchangeable_product?: InterchangeableProduct
    brand?: Brand
    status: ProductStatus = "Active"

}