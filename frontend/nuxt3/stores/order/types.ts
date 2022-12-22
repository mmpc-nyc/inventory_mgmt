import {Order} from "~/models/order";

export class OrderState {
    order: Order | null = null
    orders: Order[] = []
}