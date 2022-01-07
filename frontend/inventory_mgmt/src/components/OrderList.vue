<template>
  <ul class="order-list">
    <order-list-item v-for="order in orders" :key="order.key" :order="order"></order-list-item>
  </ul>
</template>
<script>
import OrderListItem from "@/components/OrderListItem"

export default {
  name: "OrderList",
  components: {OrderListItem},
  props: ["orders"]
}
</script>