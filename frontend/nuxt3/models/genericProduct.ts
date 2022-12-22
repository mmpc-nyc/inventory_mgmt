import {Category} from "./category";

type GenericProductStatus = "Active" | "Inactive"

export class GenericProduct {
    category?: Category
    name: string = ""
    status: GenericProductStatus = "Active"
}