<template>
  <li>{{ customer_name }}</li>
  <li></li>

</template>

<script>
export default {
  name: "AdminCustomerListItem",
  props: ["customer"],
  computed: {
    customer_name(){
      if (!this.customer.company_name){
        return `${this.customer.first_name} ${this.customer.last_name}`
      }
      return this.customer.company_name
    }
  }
}
</script>

<style scoped>

</style>