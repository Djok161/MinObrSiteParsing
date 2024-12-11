<!-- src/views/HomePage.vue -->
<template>
  <div class="container mt-5">
    <ModalComponent
        title="Добавление нового сайта для проверки"
        @confirm="handleConfirm"
    >
    </ModalComponent>
    <ListCards />
  </div>
</template>

<script>
import ModalComponent from '../components/modals/ModalComponent.vue';
import ListCards from "@/components/ListCards.vue"; // Убедитесь, что путь верный

export default {
  components: {
    ListCards,
    ModalComponent,
  },
  methods: {
    handleConfirm() {
      alert('Изменения сохранены!');
    },
  },
};
</script>
