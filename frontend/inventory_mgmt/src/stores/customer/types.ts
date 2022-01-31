import {Customer} from "@/models/customer";


export class CustomerState {
    customer: Customer | null = null
    customers: Customer[] = []
}