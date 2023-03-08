export class Brand{
    id?: number
}

export type MaterialStatus = "Active" | "Inactive" | "Recall"

export class Material{
    id?: number
    brand?: Brand
    status: MaterialStatus = "Active"

}