import {Customer} from "~/models/customer";
import {User} from "~/models/user";
import {Equipment} from "~/models/equipment";
import {Location} from "~/models/location";

export type OrderActivity = "Deploy" | "Collect" | "Inspect"
export type OrderStatus = "New" | "Assigned" | "In Progress" | "Completed" | "Canceled"

const ORDER_ACTIVITIES: {value: OrderActivity, label: string}[] = [
    {
        value: "Deploy",
        label: "Deploy"
    },
    {
        value: "Collect",
        label: "Collect"
    },
    {
        value: "Inspect",
        label: "Inspect"
    }
]

export class Order {
    id?: number
    activity: OrderActivity = "Deploy"
    customer?: Customer
    status: OrderStatus = "New"
    location?: Location
    equipments: Equipment[] = []
    team_lead?: User
    team: User[] = []
    date: string = ""

    getOrderActivities() {
        return ORDER_ACTIVITIES
    }
}

export class DeployOrder extends Order {
    activity: OrderActivity = "Deploy"
}

export class CollectOrder extends Order {
    activity: OrderActivity = "Collect"
}

export class InspectOrder extends Order {
    activity: OrderActivity = "Inspect"
}