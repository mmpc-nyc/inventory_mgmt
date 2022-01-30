import {Customer} from "@/models/customer";
import {User} from "@/models/user";
import {Equipment} from "@/models/equipment";
import {GenericProduct} from "@/models/genericProduct";
import {Location} from "@/models/location";

export type OrderActivity = "Deploy" | "Collect" | "Inspect"
export type OrderStatus = "New" | "Assigned" | "In Progress" | "Completed" | "Canceled"

export interface Order {
    id: number
    activity: OrderActivity
    customer: Customer
    status: OrderStatus
    location: Location
    equipments: Equipment[]
    team_lead: User
    team: User[]
    generic_products: GenericProduct[]
    date: string
}

class DeployOrder implements Order {
    id: number;
    activity: OrderActivity = "Deploy"
    status: OrderStatus;
    customer: Customer;
    location: Location;
    equipments: Equipment[];
    generic_products: GenericProduct[];
    team_lead: User;
    team: User[];
    date: string;

    constructor(
        id: number,
        customer: number | Customer,
        status: OrderStatus,
        team_lead: User,
        team: User[],
        location: Location,
        date: string,
        equipments: Equipment[],
        generic_products: GenericProduct[]
    ) {
        this.id = id
        this.status = status
        this.customer = customer
        this.location = location
        this.equipments = equipments
        this.generic_products = generic_products
        this.team_lead = team_lead
        this.team = team
        this.date = date
    }
}