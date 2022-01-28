export class User{
    username: string
    password: string
    loggedIn: boolean = true

    constructor(username: string, password: string) {
        this.username = username
        this.password = password
    }
}