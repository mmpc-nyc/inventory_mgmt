<template>
  <li>
    <span class="name">{{ equipment.name }}</span>
    <span class="category">{{ equipment.category}}</span>
    <span class="condition">{{ equipment.condition }}</span>
    <span class="status">{{ equipment.status }}</span>

    <span></span>
  </li>
</template>
<script>
export default {
  props: ["equipment"],
  methods: {}

}
</script>