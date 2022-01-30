import {Location} from "@/models/location";
import {Contact} from "@/models/contact";

type CustomerType = "Residential" | "Commercial"

export interface Customer {
    id?: number
    customer_type: CustomerType
    first_name: string
    last_name: string
    company_name?: string
    email: string
    phone_number: string
    contacts: Contact[]
    billing_location: Location
    service_locations: Location[]
    parent: Customer | null

    name(): string
    getLocation(): Location
}


export class Customer implements Customer {
    id?: number
    customer_type: CustomerType = "Residential"
    first_name: string = ""
    last_name: string = ""
    company_name?: string = ""
    email: string = ""
    phone_number: string = ""
    contacts: Contact[] = []
    billing_location: Location = new Location()
    service_locations: Location[] = []
    parent: Customer | null = null

    name() {
        if (this.customer_type) {
            return this.company_name
        }
        return [this.first_name, this.last_name].join(" ")
    }
}