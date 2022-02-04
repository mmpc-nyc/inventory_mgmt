<template>
  <ui-card v-if="newOrder">
    <section class="type">
      <h2>Order Activity</h2>
      <ui-select v-model="newOrder.activity" :options="newOrder.getOrderActivities()"></ui-select>
    </section>
    <section class="customer">
      <h2>Customer</h2>
      <ui-autocomplete
          v-model="customerSearchText"
          delay="500"
          @search="onSearchCustomer"
          @selected="onSelectCustomer"
          :source="customerSearchResults"
          :source-format="{ label: 'first_name', value: 'id'}"
          remote
          fullwidth
      ></ui-autocomplete>
      <admin-order-create-customer-detail v-if="newOrder.customer" :customer="newOrder.customer"
                                          class="customer-details">
      </admin-order-create-customer-detail>
    </section>
    <section v-if="newOrder.customer" class="location">
      <h2>Location</h2>
      <ui-autocomplete
          :source="newOrder.customer.service_locations"
          :source-format="{label: 'name', value:'id'}"
          fullwidth
      >
      </ui-autocomplete>
    </section>
    <section class="generic-products"><h2>Generic Products</h2></section>
    <section class="equipments"><h2>Equipment</h2></section>
    <section class="date"><h2>Date</h2></section>
    <section class="team"><h2>Team</h2></section>
  </ui-card>

</template>

<script>

import customerService from "@/services/CustomerService.ts";
import AdminOrderCreateCustomerDetail from "@/components/admin/AdminOrderCreateCustomerDetail";

export default {
  name: "AdminOrderCreate",
  components: {AdminOrderCreateCustomerDetail},
  props: ["order"],
  data() {
    return {
      newOrder: {},
      customerSearchText: "",
      customerSearchResults: [],
    }
  },
  created() {
    this.newOrder = this.order
  },
  methods: {
    async onSearchCustomer(text) {
      this.customerSearchResults = await customerService.search(text)
    },
    onSelectCustomer(customer) {
      this.newOrder.customer = customer
    }

  },
  watch: {
    newOrder: {
      handler: function (before, after) {
        this.$emit('orderUpdated', after)
      },
      deep: true
    }
  }
}
</script>

<style scoped>

</style>