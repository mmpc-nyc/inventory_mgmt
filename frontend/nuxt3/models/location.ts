export class LocationState{
    name: string = ""
}

export class Location{
    id?: number
    street_address: string = ""
    address_line_2: string = ""
    city: string = ""
    state?: LocationState
    postal_code: string = ""
    latitude?: number
    longitude?: number
}