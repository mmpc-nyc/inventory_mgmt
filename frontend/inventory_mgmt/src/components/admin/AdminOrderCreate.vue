<template>
  <ui-card v-if="newOrder">
    <section class="date">
      <h2>Date</h2>
      <ui-datepicker
          v-model="newOrder.date"
          :config="config"
          placeholder="Select Datetime.."
          toggle
          clear
      >
        <template #toggle>
          <i class="fa fa-calendar"></i>
        </template>
        <template #clear>
          <i class="fa fa-close"></i>
        </template>
      </ui-datepicker>
    </section>
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
    <section v-if="newOrder.customer">
      <h2>Service Location {{ newOrder.location ? newOrder.location.name : "" }}</h2>
      <admin-order-create-location-selection
          :locations="newOrder.customer.service_locations"
          @onSelectLocation="onSelectLocation"
      ></admin-order-create-location-selection>
    </section>
    <section v-if="newOrder.activity === 'Deploy'" class="generic-products">
      <h2>Generic Products</h2>
    <ui-autocomplete
          v-model="genericProductSearchText"
          delay="500"
          @search="onSearchGenericProduct"
          @selected="onSelectGenericProduct"
          :source="genericProductSearchResults"
          :source-format="{ label: 'name', value: 'id'}"
          remote
          fullwidth></ui-autocomplete>
    </section>
    <section class="equipments"><h2>Equipment</h2></section>
    <ui-autocomplete
          v-model="equipmentSearchText"
          delay="500"
          @search="onSearchEquipment"
          @selected="onSelectEquipment"
          :source="equipmentSearchResults"
          :source-format="{ label: 'name', value: 'id'}"
          remote
          fullwidth></ui-autocomplete>
    <section class="team"><h2>Team</h2></section>
  </ui-card>

</template>

<script>

import customerService from "@/services/CustomerService.ts";
import AdminOrderCreateCustomerDetail from "@/components/admin/AdminOrderCreateCustomerDetail";
import AdminOrderCreateLocationSelection from "./AdminOrderCreateLocationSelection";
import genericProductService from "../../services/GenericProductService";
import equipmentService from "../../services/EquipmentService";

export default {
  name: "AdminOrderCreate",
  components: {AdminOrderCreateLocationSelection, AdminOrderCreateCustomerDetail},
  props: ["order"],
  data() {
    return {
      newOrder: {},
      customerSearchText: "",
      customerSearchResults: [],
      equipmentSearchText: "",
      equipmentSearchResults: [],
      genericProductSearchText: "",
      genericProductSearchResults: [],
      config: {
        enableTime: true,
        dateFormat: 'Y-m-d H:i'
      },
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
    },
    onSelectLocation(location) {
      this.newOrder.location = location
    },
    onSelectEquipment(equipment){
      console.log(equipment)
    },
    async onSearchEquipment(text) {
      this.equipmentSearchResults = await equipmentService.search(text)
      console.log(text)
    },
    onSelectGenericProduct(genericProduct){
      console.log(genericProduct)
    },
    async onSearchGenericProduct(text) {
      this.genericProductSearchResults = await genericProductService.search(text)
      console.log(text)
    },
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