<template>
  {{ customer}}
</template>

<script>
export default {
  name: "CustomerAdminDetail.vue",
  props: ["id"],
  computed: {
    customer() {
      return this.$store.state.customers.customer
    }
  },
  mounted() {
    this.$store.dispatch('customers/getOne', this.$route.params['id'])
  }
}
</script>

<style scoped>

</style>