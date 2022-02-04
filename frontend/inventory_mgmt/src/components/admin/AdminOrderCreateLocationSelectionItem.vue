<template>
  <ui-item @click="onSelectLocation" :class="{selected:location.selected }">
    {{ location.address_line_1 }}
  </ui-item>
</template>

<script>
export default {
  name: "AdminOrderCreateLocationSelectionItem",
  props: ["location"],
  methods: {
    onSelectLocation() {
      this.$emit("onSelectLocation", this.location)
    }
  }
}
</script>

<style scoped>
</style>