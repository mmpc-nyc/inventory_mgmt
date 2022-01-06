<template>
  <h1>Equipment Checkin</h1>
  <the-scanner @onScanSuccess="onScanSuccess"></the-scanner>
</template>
<script>
import TheScanner from '@/components/TheScanner'
export default {
  name: 'Equipment Checkin',
  components: {TheScanner},
  methods: {
    onScanSuccess(payload){
      this.$store.dispatch("equipments/checkIn", payload.decodedText)
    }
  }
}
</script>