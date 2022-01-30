import {Product} from "@/models/product";
import {Warehouse} from "@/models/warehouse";
import {User} from "@/models/user";
import {Location} from "@/models/location";


export class EquipmentCondition {
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
    name: string = ''
    product?: Product
    status: EquipmentStatus = "Picked Up"
    warehouse?: Warehouse
    condition?: EquipmentCondition
    user?: User
    location?: Location
}