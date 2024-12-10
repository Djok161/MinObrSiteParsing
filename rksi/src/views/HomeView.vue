<template>
  <div class="container mt-5">
    <button
        type="button"
        class="btn btn-primary"
        data-bs-toggle="modal"
        data-bs-target="#exampleModal"
    >
      Новый сайт
    </button>

    <ListCards />

    <!-- Подключение модального окна -->
    <ModalComponent
        title="Добавление нового сайта для проверки"
        @confirm="handleConfirm"
    >
    </ModalComponent>
  </div>
</template>

<script>
import ModalComponent from '../components/modals/ModalComponent.vue';
import CardComponent from '../components/CardComponent.vue';
import ListCards from "@/components/ListCards.vue";

export default {
  components: {
    ListCards,
    ModalComponent,
    CardComponent
  },
  methods: {
    handleConfirm() {
      alert('Изменения сохранены!');
    },
  },
};
</script>
