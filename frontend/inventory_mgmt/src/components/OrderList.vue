<template>
  <order-list-item v-for="[id, order] in orders" :key="order.key" :id="id" :order="order"></order-list-item>
</template>
<script>
import OrderListItem from "@/components/OrderListItem"
export default {
  name: "OrderList",
  components: {OrderListItem},
  props: ["orders"]
}
</script>