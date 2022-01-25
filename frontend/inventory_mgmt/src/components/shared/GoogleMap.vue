<template>
  <GMapMap
      :center="geolocation"
      :zoom="16"
      :options="mapOptions"
      map-type-id="terrain"
  >
    <GMapMarker :position="geolocation"></GMapMarker>
  </GMapMap>

</template>

<script>
export default {
  name: "GoogleMap",
  data() {
    return {
      mapOptions: {
        zoomControl: true,
        mapTypeControl: false,
        streetViewControl: false,
        fullscreenControl: false
      }
    }
  },
  methods: {
    setPlace(result) {
      this.geolocation.lat = result.geometry.location.lat()
      this.geolocation.lng = result.geometry.location.lng()
      let formatted_address = result.formatted_address
      let name = result.name
      console.log(result, formatted_address, name)
    }

  },
  props: ["geolocation"],
}
</script>

<style scoped lang="scss">
.vue-map-container {
  height: 300px;
  width: 300px;
}
</style>