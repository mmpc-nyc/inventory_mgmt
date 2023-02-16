import {Category} from "./category";

type InterchangeableProductStatus = "Active" | "Inactive"

export class InterchangeableProduct {
    category?: Category
    name: string = ""
    status: InterchangeableProductStatus = "Active"
}