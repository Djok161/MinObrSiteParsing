<template>
  <div class="container mt-4">
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
    </div>
    <div v-else>
      <div v-if="error" class="alert alert-danger">
        {{ error }}
      </div>
      <div class="row">
        <div
            class="col-md-6 mb-4"
            v-for="card in cards"
            :key="card.id"
        >
          <Card
              :card="card"
              @refresh="handleRefresh"
              @delete="handleDelete"
              @navigate="handleNavigate"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Card from '../components/CardComponent.vue';
import api from '../services/api.js';

export default {
  name: 'ListCards',
  components: { Card },
  data() {
    return {
      cards: [],
      loading: false,
      error: null,
    };
  },
  created() {
    this.fetchCards();
  },
  methods: {
    async fetchCards() {
      this.loading = true;
      try {
        const response = await api.get('/cards/all');
        this.cards = response.data;
      } catch (err) {
        this.error = 'Не удалось загрузить карточки.';
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    handleRefresh(card) {
      console.log(`Обновление карточки: ${card.name}`);
      this.fetchCards();
    },
    async handleDelete(card) {
      try {
        const response = await api.delete(`/cards/${card.id}`);
        if (response.status === 200) {
          this.cards = this.cards.filter((c) => c.id !== card.id);
          alert(`Карточка "${card.name}" успешно удалена.`);
        } else {
          alert(`Не удалось удалить карточку "${card.name}".`);
        }
      } catch (error) {
        console.error('Ошибка при удалении карточки:', error);
        alert('Произошла ошибка при удалении карточки.');
      }
    },
    handleNavigate(card) {
      alert(`Переход на страницу карточки "${card.name}".`);
    },
  },
};
</script>
