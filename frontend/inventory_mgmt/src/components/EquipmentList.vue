<template>
  <ul>
    <EquipmentListItem
        v-for="[id, equipment] in equipments"
        :key="equipment.id"
        :equipment="equipment"
        :id="id"
    ></EquipmentListItem>
  </ul>
</template>
<script>
import EquipmentListItem from "@/components/EquipmentListItem";

export default {
  name: 'EquipmentList',
  components: {EquipmentListItem},
  props: ["equipments"],
}

</script>