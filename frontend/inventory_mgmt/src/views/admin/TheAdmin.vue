<template>
  <main>
      <router-link :to="{name: 'admin_customer_list'}">Customers</router-link>
      <router-view/>
  </main>
</template>

<script>
export default {
  name: "TheAdmin"
}
</script>

<style scoped>

</style>