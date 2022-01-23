<template>
  <ui-drawer nav-id="top-app-bar" type="modal">
    <ui-drawer-header>
      <ui-drawer-title>Admin</ui-drawer-title>
    </ui-drawer-header>
    <ui-drawer-content>
      <ui-nav>
        <router-link custom v-slot="{isActive, href, navigate}" :to="{name:'admin_customer'}">
          <ui-nav-item :active="isActive" :href="href" @click="navigate">Customers</ui-nav-item>
        </router-link>
      </ui-nav>
    </ui-drawer-content>
  </ui-drawer>
  <router-view/>
</template>

<script>

export default {
  name: "TheAdmin",
  components: {}
}
</script>

<style scoped>

</style>