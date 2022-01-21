<template>
  <main>
    <customer-list :customers="customers"></customer-list>
    <router-link :to="{name: 'admin_customer_create'}">Create</router-link>
    <router-view/>
  </main>
</template>

<script>
import CustomerList from "@/components/admin/CustomerList";

export default {
  name: "CustomerAdmin",
  components: {CustomerList},
  computed: {
    customers() {
      return this.$store.state.customers.customers
    }
  },
  mounted() {
    this.$store.dispatch("customers/getCustomerList")
  },
}
</script>