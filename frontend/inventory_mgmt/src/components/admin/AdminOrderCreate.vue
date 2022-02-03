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
      <div  v-if="newOrder.customer"  class="customer-details">
        <span>{{newOrder.customer.first_name}}</span>
      </div>
    </section>
    <section v-if="newOrder.customer" class="location"><h2>Location</h2>
    </section>
    <section class="generic-products"><h2>Generic Products</h2></section>
    <section class="equipments"><h2>Equipment</h2></section>
    <section class="date"><h2>Date</h2></section>
    <section class="team"><h2>Team</h2></section>
  </ui-card>

</template>

<script>

import customerService from "@/services/CustomerService.ts";

export default {
  name: "AdminOrderCreate",
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
  methods:{
    async onSearchCustomer(text){
      console.log(text)
      let searchResults =  await customerService.search(text)
      this.customerSearchResults = searchResults.data
    },
    onSelectCustomer(customer){
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