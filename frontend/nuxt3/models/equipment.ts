import {Product} from "~/models/product";
import {StockLocation} from "~/models/warehouse";
import {User} from "~/models/user";
import {Location} from "~/models/location";


export class EquipmentCondition {
    id?: number
    name: string = ''
    description: string = ''
    action_collect: boolean = false
    action_decommission: boolean = false
    action_deploy: boolean = false
    action_store: boolean = false
    action_transfer: boolean = false
    action_withdraw: boolean = false
}

export type EquipmentStatus = "Stored" | "Deployed" | "Picked Up" | "Missing" | "Decommissioned"

export class Equipment {
    id?: number
    name: string = ''
    product?: Product
    status: EquipmentStatus = "Picked Up"
    warehouse?: StockLocation
    condition?: EquipmentCondition
    user?: User
    location?: Location
}