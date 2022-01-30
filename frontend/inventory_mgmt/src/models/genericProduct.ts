import {Category} from "./category";

type GenericProductStatus = "Active" | "Inactive"

export class GenericProduct {
    category: Category | null = null
    name: string = ""
    status: GenericProductStatus = "Active"
}