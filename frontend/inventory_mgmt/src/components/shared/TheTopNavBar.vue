<template>
  <nav class="top-nav-bar">
    <div class="actions">
      <ui-icon-button icon="menu"></ui-icon-button>
      <router-link to="/" custom v-slot="{navigate, isActive}">
        <ui-button text :class="{active: isActive}" @click="navigate">Home</ui-button>
      </router-link>
    </div>
    <div class="toolbar">

      <router-link :to="{name:'admin'}" custom v-slot="{navigate, isActive}">
        <ui-button text :class="{active: isActive}" @click="navigate">Admin</ui-button>
      </router-link>
      <the-user-info class="userinfo"></the-user-info>
    </div>
  </nav>
</template>

<script>
import TheUserInfo from "@/components/shared/TheUserInfo";

export default {
  name: "TheTopNavBar",
  components: {TheUserInfo}
}
</script>

<style lang="scss" scoped>
.top-nav-bar {
  display: grid;
  grid-template-areas: "actions toolbar";
  grid-template-columns: 30ch 1fr;
  align-items: center;
}

.actions {
  grid-area: actions;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.toolbar {
  grid-area: toolbar;
  justify-self: flex-end;
  display: flex;
}

</style>