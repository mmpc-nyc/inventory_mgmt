<template>
  <the-side-nav-bar>
    <ui-nav>
      <router-link custom v-slot="{isActive, href, navigate}" :to="{name:'admin_customer_list'}">
        <ui-item :active="isActive" :href="href" @click="navigate">Customers</ui-item>
      </router-link>
    </ui-nav>
  </the-side-nav-bar>
  <main>
    <div class="admin-container">
      <nav class="admin-navigation">
        <nav class="breadcrumbs" id="breadcrumbs">
          <router-link :to="{name:'admin'}" custom v-slot="{navigate, isActive}">
            <ui-button text :class="{active: isActive}" @click="navigate">Admin</ui-button>
          </router-link>
        </nav>
        <nav class="admin-actions" id="admin-actions">
          <router-link custom v-slot="{navigate}" :to="{name:'admin_customer_create'}">
            <ui-button outlined icon="add" @click="navigate">Add</ui-button>
          </router-link>
        </nav>
      </nav>
      <ui-card class="admin-content">
        <router-view/>
      </ui-card>
    </div>
  </main>
</template>

<script>
import TheSideNavBar from "@/components/shared/TheSideNavBar";

export default {
  name: "TheAdmin",
  components: {TheSideNavBar},
}
</script>

<style scoped lang="scss">
.admin-container {
  display: grid;
  grid-template-areas: "admin-navigation"
  "admin-content";
  gap: 1rem;
}

.admin-navigation {
  grid-area: admin-navigation;
  display: grid;
  grid-template-areas: "breadcrumbs admin-actions";
  grid-template-columns: 1fr 1fr;
  align-items: center;
  justify-content: space-around;
}

.admin-actions {
  grid-area: admin-actions;
  display: flex;
  align-content: end;
  align-items: center;
  justify-content: end;
}

.admin-content {
  grid-area: admin-content;
}

.breadcrumbs {
  grid-area: breadcrumbs;
}

</style>