import {PhoneNumber} from "@/models/phone_number";

export class Contact{
    id?: number
    first_name?: string
    last_name?: string
    phone_numbers?: PhoneNumber[]
}