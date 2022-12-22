export class LocationState{
    name: string = ""
}

export class Location{
    id?: number
    address_line_1: string = ""
    address_line_2: string = ""
    city: string = ""
    state?: LocationState
    postal_code: string = ""
    latitude?: number
    longitude?: number
}