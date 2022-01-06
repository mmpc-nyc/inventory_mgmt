<template>
  <li>
    <span>{{ equipment }}</span>
    <button @click="deleteEquipment(equipment)">Delete</button>
    <span></span>
  </li>
</template>
<script>
export default {
  props:
      ['equipment'],
  methods: {
    deleteEquipment(equipment){
      this.$emit('deleteEquipment',equipment)
    }
  }
}
</script>