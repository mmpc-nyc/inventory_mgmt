<template>
  <div class="location">
    <span class="location-name">{{ location.name }}</span>
    <span class="location-address-line-1">{{ location.address_line_1 }}</span>
    <span class="location-address-line-2">{{ location.address_line_2 }}</span>
    <span class="location-city">{{location.city}}</span>
    <span class="location-state">{{location.state}}</span>
    <span class="location-postal-code">{{location.postal_code}}</span>
<!--    <google-map location="location"></google-map>-->
  </div>
</template>

<script>
export default {
  name: "AdminCustomerDetailLocation",
  components: {},
  props: ["location"]
}
</script>

<style scoped>
</style>