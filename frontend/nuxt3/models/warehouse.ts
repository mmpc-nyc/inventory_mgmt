import {Location} from "~/models/location";

type StockLocationStatus = "Active" | "Inactive" | "Full"

export class StockLocation{
    id?: number
    status: StockLocationStatus = "Active"
    location?: Location
}