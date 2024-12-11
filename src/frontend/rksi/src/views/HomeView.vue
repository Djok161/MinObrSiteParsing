<!-- src/views/HomePage.vue -->
<template>
  <div class="container mt-5">
    <SubmitLink />
    <ListCards />
  </div>
</template>

<script>
import SubmitLink from '@/components/modals/ModalComponent.vue';
import ListCards from "@/components/ListCards.vue"; // Убедитесь, что путь верный

export default {
  components: {
    ListCards,
    SubmitLink,
  },
};
</script>

<style scoped>
/* Ваши стили здесь */
</style>
