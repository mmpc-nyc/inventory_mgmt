<template>
  <the-header></the-header>
  <main>
    <router-view/>
  </main>
  <the-footer></the-footer>

</template>

<script>
import TheHeader from "@/components/shared/TheHeader";
import TheFooter from "@/components/shared/TheFooter";
export default {
  name: "AdminCustomer",
  components: {TheFooter, TheHeader}
}
</script>

<style scoped>

</style>