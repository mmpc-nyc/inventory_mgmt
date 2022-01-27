<template>
  <teleport to="#header">
    <h1 :class="$tt('headline3')">Customer Detail</h1>
  </teleport>
</template>

<script>
export default {
  name: "CustomerAdminDetail.vue",
  props: ["customer"],
}
</script>

<style scoped>

</style>