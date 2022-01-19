<template>
  Hello World
  <equipment-list :equipments="equipments"></equipment-list>
</template>
<script>
import EquipmentList from '@/components/inventory/EquipmentList'

export default {
  components: {EquipmentList},
  computed: {
    equipments() {
      return this.$store.state.equipments.equipments
    }
  },
  mounted() {
    this.$store.dispatch("equipments/getList")
  },
}
</script>