<template>
  <main>
      <router-link :to="{name: 'customers_admin'}">Customers</router-link>
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