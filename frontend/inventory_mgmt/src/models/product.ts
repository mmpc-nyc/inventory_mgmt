import {GenericProduct} from "./genericProduct";

export class Brand{
    id?: number
}

export type ProductStatus = "Active" | "Inactive" | "Recall"

export class Product{
    id?: number
    generic_product?: GenericProduct
    brand?: Brand
    status: ProductStatus = "Active"

}