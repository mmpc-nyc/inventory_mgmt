<template>
  <ui-list>
    <ui-item class="headers customer-list-item">
      <span class="id">ID</span>
      <span class="name">Customer Name</span>
      <span class="type">Type</span>
      <span class="email">Email</span>
      <span class="phone-number">Phone</span>
      <span class="actions">Actions</span>
    </ui-item>
    <admin-customer-list-item v-for="customer in customers" :customer="customer"
                              :key="customer.id"></admin-customer-list-item>
  </ui-list>
</template>

<script>
import AdminCustomerListItem from "@/components/admin/AdminCustomerListItem";

export default {
  name: "AdminCustomerList",
  props: ["customers"],
  components: {AdminCustomerListItem}
}
</script>
<style lang="scss">

.customer-list-item {
  display: grid;
  grid-template-areas: "id type name email phone-number actions";
  grid-template-columns: 10ch 12ch 1fr 30ch 12ch 25ch;
  align-items: center;
  justify-items: start;
}

.id {
  grid-area: id
}

.name {
  grid-area: name
}

.type {
  grid-area: type
}

.email {
  grid-area: email
}

.phone-number {
  grid-area: phone-number
}

.actions {
  width:100%;
  grid-area: actions;
  display: flex;
  justify-content: space-evenly;
}
</style>