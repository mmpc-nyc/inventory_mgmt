<template>
  <admin-order-create :order="order" @orderUpdated="updateOrder"></admin-order-create>
</template>

<script>
import {Order} from "@/models/order.ts";
import AdminOrderCreate from "@/components/admin/AdminOrderCreate";

export default {
  name: "AdminOrderCreateView",
  components: {AdminOrderCreate},
  data() {
    return {
      order: new Order()
    }
  },
  methods: {
    updateOrder(newOrder) {
      this.order = newOrder
    }
  }
}
</script>

<style scoped>

</style>