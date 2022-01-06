<template>
  <ul>
    <EquipmentListItem
        v-for="equipment in equipments"
        :key="equipment.id"
        :equipment="equipment"
        @deleteEquipment="deleteEquipment"
    ></EquipmentListItem>
  </ul>
</template>
<script>
import axios from 'axios';
import EquipmentListItem from "@/views/EquipmentListItem";

export default {
  components: {EquipmentListItem},
  data: function () {
    return {
      equipments: null
    }
  },
  async created() {
    this.equipments = await this.getEquipmentList()
  },
  methods: {
    async getEquipmentList() {
      const response = await axios.get('http://localhost:8000/api/brands/')
      return response.data;
    },
    deleteEquipment(equipment) {
      axios.delete(`http://localhost:8000/api/brands/${equipment.id}`)
          .then((response) => {
                console.log(response);
              }
          )
      this.equipments = this.equipments.filter((eq) => {
        console.log(equipment.id)
        return eq.id !== equipment.id
      })
    }
  }
}

</script>