import { AuthState } from "./auth/types";
import { CustomerState } from "./customer/types";
import { EquipmentState } from "./equipment/types";
import { UserState } from "./user/types";

export interface RootState {
    auth: AuthState,
    equipments: EquipmentState,
    users: UserState,
    customers: CustomerState
}