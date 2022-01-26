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
  computed: {
    geolocation() {
      if (!this.location.latitude || !this.location.longitude) {
        return this.$config.DEFAULT_LAT_LNG
      }
      return {
        lat: this.location.latitude,
        lng: this.location.longitude
      }
    }
  },
  props: ["location"],
}
</script>

<style scoped lang="scss">
.vue-map-container {
  height: 300px;
  width: 300px;
}
</style>