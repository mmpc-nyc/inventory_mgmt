<template>
  <admin-customer-list :customers="customers"></admin-customer-list>

</template>

<script>
import AdminCustomerList from "@/components/admin/AdminCustomerList";

export default {
  name: "AdminCustomers",
  components: {AdminCustomerList},
  computed: {
    customers() {
      return this.$store.state.customers.customers
    }
  },
  mounted() {
    this.$store.dispatch("customers/getList")
  },
}
</script>