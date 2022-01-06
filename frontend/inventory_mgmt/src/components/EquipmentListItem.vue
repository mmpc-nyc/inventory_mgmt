<template>
  <li>
    <span class="actions"><button @click="remove"><i class="material-icons">delete</i> </button></span>
    <span class="name">{{ equipment.name }}</span>
    <span class="category">{{ equipment.category}}</span>
    <span class="condition">{{ equipment.condition }}</span>
    <span class="status">{{ equipment.status }}</span>

    <span></span>
  </li>
</template>
<script>
export default {
  props: ["equipment", "id"],
  methods: {
    remove(){
      this.$store.commit("equipments/delete", this.equipment)
    }
  }

}
</script>