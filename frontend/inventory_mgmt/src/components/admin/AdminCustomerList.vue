<template>
  <ul>
    <admin-customer-list-item v-for="customer in customers" :customer="customer" :key="customer.id"></admin-customer-list-item>
  </ul>
</template>

<script>
import AdminCustomerListItem from "@/components/admin/AdminCustomerListItem";

export default {
  name: "AdminCustomerList",
  props: ["customers"],
  components: {AdminCustomerListItem}
}
</script>