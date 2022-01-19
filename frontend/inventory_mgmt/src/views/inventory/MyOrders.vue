<template>
  <router-link to="create_order_form">Create Order</router-link>
  <order-list :orders="orders"></order-list>
</template>
<script>
import OrderList from '@/components/inventory/OrderList'

export default {
  name: "MyOrders",
  components: {OrderList},
  computed: {
    orders() {
      return this.$store.state.orders.orders
    }
  },
  mounted() {
    this.$store.dispatch("orders/getOrderList")
  },
}
</script>