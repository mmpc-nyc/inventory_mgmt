<template>
  <ul>
    <EquipmentListItem
        v-for="equipment in equipments"
        :key="equipment.id"
        :equipment="equipment"
    ></EquipmentListItem>
  </ul>
</template>
<script>
import EquipmentListItem from "@/components/EquipmentListItem";

export default {
  components: {EquipmentListItem},
  props: ["equipments"],
}

</script>