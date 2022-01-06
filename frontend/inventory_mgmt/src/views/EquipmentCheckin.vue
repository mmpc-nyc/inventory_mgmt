<template>
  <h1>Equipment Checkin</h1>
  <the-scanner @onScanSuccess="onScanSuccess"></the-scanner>
  <equipment-list :equipments="equipments"></equipment-list>
</template>
<script>
import TheScanner from '@/components/TheScanner'
import EquipmentList from "@/components/EquipmentList";

export default {
  name: 'Equipment Checkin',
  components: {EquipmentList, TheScanner},
  computed: {
    equipments() {
      return this.$store.state.equipments.equipments
    }
  },
  methods: {
    onScanSuccess(payload) {
      this.$store.dispatch("equipments/checkIn", payload.decodedText)
    }
  }
}
</script>