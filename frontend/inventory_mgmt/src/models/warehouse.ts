import {Location} from "@/models/location";

type WarehouseStatus = "Active" | "Inactive" | "Full"

export class Warehouse{
    id?: number
    status: WarehouseStatus = "Active"
    location?: Location
}