<template>
  <ui-item class="customer-list-item">
    <span class="id">{{ customer.id }}</span>
    <router-link custom v-slot="{navigate}" :to="{name:'admin_customer_detail', params:{id:customer.id}}">
      <ui-button @click="navigate" class="customer-name">{{ customer_name }}</ui-button>
    </router-link>
    <span class="email">{{ customer.email }}</span>
    <span class="phone-number">{{ customer.phone_number }}</span>
    <span class="actions">
        <ui-button outlined icon="add">Schedule Order</ui-button>
      </span>
  </ui-item>
</template>

<script>
export default {
  name: "AdminCustomerListItem",
  props: ["customer"],
  computed: {
    customer_name() {
      if (!this.customer.company_name) {
        return `${this.customer.first_name} ${this.customer.last_name}`
      }
      return this.customer.company_name
    }
  }
}
</script>

<style scoped lang="scss">
</style>