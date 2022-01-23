<template>
  <router-link custom v-slot="{navigate}" :to="{name:'admin_customer_create'}">
    <ui-button outlined icon="add" @click="navigate">Add</ui-button>
  </router-link>
  <router-view/>

</template>

<script>
export default {
  name: "AdminCustomerIndex"
}
</script>

<style scoped>

</style>