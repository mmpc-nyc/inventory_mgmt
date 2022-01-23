<template>
  <the-side-nav-bar>
    <ui-nav>
      <router-link custom v-slot="{isActive, href, navigate}" :to="{name:'admin_customer_list'}">
        <ui-item :active="isActive" :href="href" @click="navigate">Customers</ui-item>
      </router-link>
    </ui-nav>
  </the-side-nav-bar>
  <main>
    <router-view/>
  </main>
</template>

<script>
import TheSideNavBar from "@/components/shared/TheSideNavBar";

export default {
  name: "TheAdmin",
  components: {TheSideNavBar},
}
</script>

<style scoped>
</style>