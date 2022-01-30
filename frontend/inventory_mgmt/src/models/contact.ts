export interface PhoneNumber {
    id: number
    phone_number: string
}

export class Email {
    id?: number
    email: string = ""
}


export class Contact {
    id?: number
    first_name: string = ""
    last_name: string = ""
    phone_numbers: PhoneNumber[] = []
    emails: Email[] = []
}