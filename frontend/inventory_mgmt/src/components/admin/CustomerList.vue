<template>
  <ul>
    <customer-list-item v-for="customer in customers" :customer="customer" :key="customer.id"></customer-list-item>
  </ul>
</template>

<script>
import CustomerListItem from "@/components/admin/CustomerListItem";

export default {
  name: "CustomerList",
  props: ["customers"],
  components: {CustomerListItem}
}
</script>