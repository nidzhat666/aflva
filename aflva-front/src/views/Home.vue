<template>
  <Engine></Engine>
  <HomeTabsSection ></HomeTabsSection>
  <HomeStatsSection></HomeStatsSection>
  <Online :title="'Online'"></Online>
  <Online :title="'Booked Flights'"></Online>
</template>

<script>

import Engine from "@/components/Engine";
import HomeTabsSection from "@/components/HomeTabsSection";
import HomeStatsSection from "@/components/HomeStatsSection";
import Online from "@/components/Online";

export default {
  name: 'Home',
  components: {
    Engine, HomeTabsSection, HomeStatsSection, Online
  }
}
</script>
