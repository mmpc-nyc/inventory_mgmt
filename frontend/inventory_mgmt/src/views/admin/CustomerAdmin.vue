<template>
  <main>
    <h1>Customer Admin</h1>
  <customer-list :customers="customers"></customer-list>
  </main>
</template>

<script>
import CustomerList from "@/components/admin/CustomerList";
export default {
  name: "CustomerAdmin",
  components: {CustomerList},
  computed:{
    customers(){
      return this.$store.state.customers.customers
    }
  },
  mounted() {
    this.$store.dispatch("customers/getCustomerList")
  },
}
</script>