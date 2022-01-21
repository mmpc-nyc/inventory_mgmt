<template>
    <router-link :to="{name: 'admin_customer_list'}">Customers</router-link>
  <router-view/>
</template>

<script>
export default {
  name: "TheAdmin"
}
</script>

<style scoped>

</style>