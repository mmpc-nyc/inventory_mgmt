export class AuthUser {
    username: string
    loggedIn: boolean
    access: string
    refresh: string

    constructor(username: string, loggedIn: boolean, access: string, refresh: string) {
        this.username = username
        this.loggedIn = loggedIn
        this.access = access
        this.refresh = refresh
    }
}

export const anonUser = new AuthUser('anonymous', false, '', '')