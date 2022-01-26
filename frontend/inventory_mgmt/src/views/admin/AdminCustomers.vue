<template>
  <h1 :class="$tt('headline3')">Customers</h1>
  <admin-customer-list :customers="customers"></admin-customer-list>
  {{customers}}

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
    this.$store.dispatch("customers/getCustomerList")
  },
}
</script>