<script setup lang="ts">
import {RouterLink, RouterView} from 'vue-router'
import LogoComponent from "@/components/LogoComponent.vue";
</script>

<template>
    <div class="container">
        <nav class="navbar">
            <RouterLink to="/" class="navbar__logo">
                <LogoComponent />
                <span class="navbar__link_nohover">HomeLab</span>
            </RouterLink>

            <RouterLink to="/about" class="navbar__link" active-class="navbar__link--active">
                About
            </RouterLink>
            <RouterLink to="/iot" class="navbar__link" active-class="navbar__link--active">
                IoT
            </RouterLink>
        </nav>
        <main class="main-content">
            <!-- Main content -->
            <RouterView />
        </main>
    </div>
</template>
<style lang="scss" scoped>
@import 'assets/colors';

.navbar {
  height: 100vh;
  width: 250px;
  background-color: $dark-header-background;
  color: $dark-text;
  padding: 1rem;
  overflow-y: auto;

  &__logo {
    display: flex;
    padding: 0.5rem;
    align-items: center;
    margin-bottom: 1rem;
    border-radius: 4px;
    text-decoration: none;

    svg {
      width: 50px;
      height: 50px;
    }

    &:hover {
      background-color: $dark-row-hover-background;
    }
  }

  &__menu {
    list-style-type: none;
    padding: 0;
    margin: 0;
  }

  &__item {
    margin-bottom: 0.5rem;
  }

  &__link {
    display: block;
    padding: 0.75rem;
    color: $dark-text;
    text-decoration: none;
    border-radius: 4px;
    transition: background-color 0.3s;

    &:hover {
      background-color: $dark-row-hover-background;
    }

    &--active {
      background-color: $dark-row-even-background;
      font-weight: bold;
    }
  }

  &__link_nohover {
    display: block;
    padding: 0.75rem;
    color: $dark-text;
    text-decoration: none;
    border-radius: 4px;
  }

  &__submenu {
    list-style-type: none;
    padding-left: 1rem;
    margin-top: 0.5rem;
  }

  &__subitem {
    margin-bottom: 0.25rem;
  }

  &__sublink {
    display: block;
    padding: 0.5rem;
    color: $dark-text;
    text-decoration: none;
    border-radius: 4px;
    transition: background-color 0.3s;

    &:hover {
      background-color: $dark-row-hover-background;
    }
  }
}
.container {
  display: flex;
}

.navbar {
  width: 250px; /* Adjust the width as needed */
}

.main-content {
  flex-grow: 1;
  padding-left: 1rem; /* Add some spacing between the navbar and content */
  padding-right: 1rem;
}
</style>
