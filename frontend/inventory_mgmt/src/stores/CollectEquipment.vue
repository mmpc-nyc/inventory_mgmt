<template>
  <qr-scanner></qr-scanner>
  <scanned-list-item></scanned-list-item>

</template>

<script>
import QrScanner from "../components/TheScanner";
import ScannedListItem from "../components/ScannedListItem";
export default {
  name: "CollectEquipment",
  components: {ScannedListItem, QrScanner}
}
</script>