<template>
  <ui-card v-if="customer">
    <h2>{{ customer.name() }}</h2>
    <span>Customer Type: {{ customer.customer_type }}</span>
    <span>Email {{ customer.email }}</span>
    <span>Phone: {{ customer.phone_number }}</span>
    <section class="billing-location" v-if="customer.billing_location">
      <h3>Billing Location</h3>
      <admin-customer-detail-location :location="customer.billing_location"></admin-customer-detail-location>
    </section>
    <section class="service-locations">
      <h3>Service Locations</h3>
      <admin-customer-detail-location v-for="location in customer.service_locations" :location="location"
                                      :key="location.id"></admin-customer-detail-location>
    </section>
  </ui-card>

</template>

<script lang="ts">
import AdminCustomerDetailLocation from "@/components/admin/AdminCustomerDetailLocation.vue";

export default {
  name: "AdminCustomerDetail",
  components: {AdminCustomerDetailLocation},
  props: ["customer"],
}
</script>

<style scoped>

</style>