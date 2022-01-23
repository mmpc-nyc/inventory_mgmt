<template>
  <customer-list :customers="customers"></customer-list>

</template>

<script>
import CustomerList from "@/components/admin/CustomerList";

export default {
  name: "AdminCustomerList",
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