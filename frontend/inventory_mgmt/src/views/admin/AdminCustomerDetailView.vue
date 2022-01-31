<template>
  <admin-customer-detail :customer="customer"></admin-customer-detail>
</template>

<script type="ts">
import AdminCustomerDetail from "@/components/admin/AdminCustomerDetail";

export default {
  name: "AdminCustomerDetailView",
  data() {
    return {}
  },
  components: {AdminCustomerDetail},
  props: ["id"],
  computed: {
    customer() {
      return this.$store.state.customers.customer
    }
  },
  created() {
    this.$store.dispatch('customers/getOne', this.$route.params['id'])
  }
}

</script>

<style scoped>

</style>