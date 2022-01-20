<template>
  <li>
    {{ customer.first_name }} {{ customer.last_name }}</li>

</template>

<script>
export default {
  name: "CustomerListItem",
  props: ["customer"]
}
</script>

<style scoped>

</style>