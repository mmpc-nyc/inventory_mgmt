<template>
  <h1 :class="$tt('headline3')">{{ customer }}</h1>
</template>

<script>
export default {
  name: "CustomerAdminDetail.vue",
  props: ["customer"],
}
</script>

<style scoped>

</style>