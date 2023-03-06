export class Brand{
    id?: number
}

export type ProductStatus = "Active" | "Inactive" | "Recall"

export class Product{
    id?: number
    brand?: Brand
    status: ProductStatus = "Active"

}