<template>
  <div class="customer-detail">
    <span class="customer-name">{{ customer.name() }}</span>
    <span class="customer-email">{{ customer.email }}</span>
    <span class="customer-phone">{{ customer.phone_number }}</span>
  </div>

</template>

<script>
import {Customer} from "@/models/customer.ts";

export default {
  name: "AdminOrderCreateCustomerDetail",
  props: {customer: Customer}
}
</script>

<style scoped>

</style>