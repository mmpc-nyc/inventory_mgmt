<template>
  <qr-scanner></qr-scanner>
  <scanned-list-item></scanned-list-item>

</template>

<script>
import QrScanner from "../components/inventory/TheScanner";
import ScannedListItem from "../components/inventory/ScannedListItem";
export default {
  name: "CollectEquipment",
  components: {ScannedListItem, QrScanner}
}
</script>