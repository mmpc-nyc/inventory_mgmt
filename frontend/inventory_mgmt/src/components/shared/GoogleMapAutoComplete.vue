<template>
  <GMapAutocomplete @place_changed="setLocation"></GMapAutocomplete>

</template>

<script>
export default {
  name: "GoogleMapAutoComplete",
  props: ["location"],
  methods: {
    setLocation(place) {

      let postal_code = null
      let city = null
      let state = null
      place.address_components.forEach(component => {
        if (component.types?.[0] === "postal_code") {
          postal_code = component.long_name
        } else if (component.types?.[0] === "administrative_area_level_1") {
          state = component.long_name
        } else if (component.types?.[0] === "administrative_area_level_2" && city == null) {
          city = component.long_name
        } else if (component.types?.[1] === "sublocality") {
          city = component.long_name
        }
      })

      let latitude = place.geometry.location.lat()
      let longitude = place.geometry.location.lng()
      this.$emit('setLocation', {
        location: this.location,
        latitude: latitude,
        longitude: longitude,
        address_line_1: place.formatted_address,
        name: place.name,
        postal_code: postal_code,
        city: city,
        state: state
      })
    }
  },
}
</script>

<style scoped>

</style>