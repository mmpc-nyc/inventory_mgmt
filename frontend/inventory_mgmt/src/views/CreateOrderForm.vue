<template>
  <form @submit="submitForm"></form>
</template>

<script>
export default {
  name: "CreateOrderForm.vue",
  methods: {
    submitForm(){
      console.log('Submit Form Pressed')
    }
  }
}
</script>

<style scoped>

</style>