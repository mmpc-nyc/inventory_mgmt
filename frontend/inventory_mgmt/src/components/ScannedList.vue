<template>
  <scanned-list-item v-for="equipment in equipments" :equipment="equipment" :key="equipment.id"></scanned-list-item>

</template>

<script>
import ScannedListItem from "./ScannedListItem";
import QrScanner from "./TheScanner";

export default {
  name: "ScannedList",
  props: "equipments",
  components: {QrScanner, ScannedListItem},
}
</script>