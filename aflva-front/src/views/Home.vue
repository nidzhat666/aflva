<template>
  <Engine></Engine>
  <HomeTabsSection ></HomeTabsSection>
  <HomeStatsSection></HomeStatsSection>
  <OnlineCardsSection></OnlineCardsSection>
  <LogosSection></LogosSection>
  <ContactUsSection></ContactUsSection>
</template>

<script>

import Engine from "@/components/Engine";
import HomeTabsSection from "@/components/sections/HomeTabsSection";
import HomeStatsSection from "@/components/sections/HomeStatsSection";
import OnlineCardsSection from "@/components/sections/OnlineCardsSection";
import LogosSection from "@/components/sections/LogosSection";
import ContactUsSection from "@/components/sections/ContactUsSection";

export default {
  name: 'Home',
  components: {
    Engine, HomeTabsSection, HomeStatsSection, OnlineCardsSection, LogosSection, ContactUsSection
  },
  mounted() {
  }
}
</script>
