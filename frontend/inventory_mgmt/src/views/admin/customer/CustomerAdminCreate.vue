<template>
  <form @submit.prevent="createCustomer">
    <button type="submit">Submit</button>
  </form>

</template>

<script>
export default {
  name: "CustomerAdminCreate",
  methods: {
    createCustomer(){
      console.log("Create Customer")
    }
  },
}
</script>

<style scoped>

</style>