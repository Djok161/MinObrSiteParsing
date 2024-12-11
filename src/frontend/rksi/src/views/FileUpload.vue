<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">Загрузка файла</h2>

    <!-- Зона для Drag-and-Drop -->
    <div
        class="dropzone"
        @click="triggerFileInput"
        @dragover.prevent="onDragOver"
        @dragleave.prevent="onDragLeave"
        @drop.prevent="onDrop"
        :class="{ 'dropzone-hover': isHovering }"
    >
      <p>Перетащите файл сюда или нажмите для выбора</p>
      <input
          type="file"
          class="file-input"
          @change="onFileSelect"
          ref="fileInput"
      />
    </div>

    <!-- Отображение выбранного файла -->
    <div v-if="file" class="mt-3">
      <p><strong>Выбран файл:</strong> {{ file.name }}</p>
      <button class="btn btn-primary" @click="uploadFile" :disabled="loading">
        {{ loading ? "Загрузка..." : "Загрузить" }}
      </button>
    </div>

    <!-- Сообщение об успехе -->
    <div v-if="successMessage" class="alert alert-success mt-3">
      {{ successMessage }}
    </div>

    <!-- Сообщение об ошибке -->
    <div v-if="errorMessage" class="alert alert-danger mt-3">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import api from "../services/api"; // Убедитесь, что ваш axios API подключен

export default {
  data() {
    return {
      file: null,
      isHovering: false,
      loading: false,
      successMessage: "",
      errorMessage: "",
    };
  },
  methods: {
    triggerFileInput() {
      // Программно вызываем клик по input при нажатии на dropzone
      this.$refs.fileInput.click();
    },
    onDragOver() {
      this.isHovering = true;
    },
    onDragLeave() {
      this.isHovering = false;
    },
    onDrop(event) {
      this.isHovering = false;
      const files = event.dataTransfer.files;
      if (files.length > 0) {
        this.file = files[0];
      }
    },
    onFileSelect(event) {
      const files = event.target.files;
      if (files.length > 0) {
        this.file = files[0];
      }
    },
    async uploadFile() {
      if (!this.file) {
        this.errorMessage = "Пожалуйста, выберите файл.";
        return;
      }

      const formData = new FormData();
      formData.append("file", this.file);

      this.loading = true;
      this.successMessage = "";
      this.errorMessage = "";

      try {
        const response = await api.post("/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        if (response.status === 200) {
          this.successMessage = "Файл успешно загружен!";
          this.file = null;
        } else {
          this.errorMessage = "Ошибка при загрузке файла.";
        }
      } catch (error) {
        console.error("Ошибка при загрузке файла:", error);
        this.errorMessage = "Ошибка при загрузке файла.";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
}

.dropzone {
  border: 2px dashed #007bff;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  color: #6c757d;
  transition: background-color 0.3s ease;
}

.dropzone-hover {
  background-color: #e9ecef;
}

.file-input {
  display: none;
}
</style>
