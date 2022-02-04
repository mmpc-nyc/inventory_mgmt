<template>
  <div class="locations">
  <ui-list v-model="selectedIndex" class="location-selection">
    <admin-order-create-location-selection-item
        v-for="(location, index) in locations"
        :location="location"
        :key="index"
        @onSelectLocation="onSelectLocation"
        class="location">
    </admin-order-create-location-selection-item>
  </ui-list>
  <google-map class="location-map" :location="locations[selectedIndex]"></google-map>
  </div>
</template>

<script>
import AdminOrderCreateLocationSelectionItem from "./AdminOrderCreateLocationSelectionItem";
import GoogleMap from "../shared/GoogleMap";

export default {
  name: "AdminOrderCreateLocationSelection",
  components: {GoogleMap, AdminOrderCreateLocationSelectionItem},
  data() {
    return {
      selectedIndex: 0
    }
  },
  methods: {
    onSelectLocation(location) {
      this.$emit("onSelectLocation", location)
    }
  },
  props: ["locations"]
}
</script>

<style scoped>
.locations {
  grid-template-areas: "selection map";
  display: grid;
  justify-content: start;
  gap:1rem;
}
.location-map{
  grid-area: map;
}
.location-selection {
  grid-area: selection;
}
</style>