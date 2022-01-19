<template>
  <li class="order-list-item">
    <span class="id">{{ order.id }}</span>
    <span class="start-date">{{ order.start_date }}</span>
    <span class="status">{{ order.status }}</span>
  </li>
</template>
<script>
export default {
  name: "OrderListItem",
  props: ["order"],
}
</script>