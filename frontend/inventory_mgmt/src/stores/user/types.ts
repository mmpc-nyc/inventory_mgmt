import {AuthUser} from "@/models/authUser";

export class UserState {
    user: AuthUser | null = null
    users: AuthUser[] = []
}