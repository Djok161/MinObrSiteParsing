<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">Загрузка PDF файла</h2>

    <!-- Loading Spinner -->
    <div v-if="isStatusLoading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
      <p>Проверка состояния сервера...</p>
    </div>

    <!-- Зона для Drag-and-Drop -->
    <div
        v-else
        class="dropzone"
        @click="triggerFileInput"
        @dragover.prevent="onDragOver"
        @dragleave.prevent="onDragLeave"
        @drop.prevent="onDrop"
        :class="{ 'dropzone-hover': isHovering, 'disabled-dropzone': !canUpload }"
        :style="{ cursor: canUpload ? 'pointer' : 'not-allowed', opacity: canUpload ? 1 : 0.6 }"
    >
      <p>Перетащите PDF файл сюда или нажмите для выбора</p>
      <input
          type="file"
          class="file-input"
          @change="onFileSelect"
          ref="fileInput"
          accept="application/pdf"
          :disabled="!canUpload"
      />
    </div>

    <!-- Отображение выбранного файла -->
    <div v-if="file" class="mt-3">
      <p><strong>Выбран файл:</strong> {{ file.name }}</p>
      <button class="btn btn-primary" @click="uploadFile" :disabled="loading || !canUpload">
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
import api from "../services/api";

export default {
  name: "FileUpload",
  data() {
    return {
      file: null,
      isHovering: false,
      loading: false,
      successMessage: "",
      errorMessage: "",
      status: "",
      isStatusLoading: true,
      pollInterval: null,
    };
  },
  computed: {
    canUpload() {
      return this.status === "ok" || this.status === "ok_run_with_mistral";
    },
  },
  methods: {
    triggerFileInput() {
      if (this.canUpload) {
        this.$refs.fileInput.click();
      }
    },
    onDragOver() {
      if (this.canUpload) {
        this.isHovering = true;
      }
    },
    onDragLeave() {
      this.isHovering = false;
    },
    onDrop(event) {
      if (!this.canUpload) return;
      this.isHovering = false;
      const files = event.dataTransfer.files;
      if (files.length > 0) {
        const selectedFile = files[0];
        if (this.isPdf(selectedFile)) {
          this.file = selectedFile;
          this.errorMessage = "";
        } else {
          this.file = null;
          this.errorMessage = "Разрешены только PDF файлы.";
        }
      }
    },
    onFileSelect(event) {
      if (!this.canUpload) return;
      const files = event.target.files;
      if (files.length > 0) {
        const selectedFile = files[0];
        if (this.isPdf(selectedFile)) {
          this.file = selectedFile;
          this.errorMessage = "";
        } else {
          this.file = null;
          this.errorMessage = "Разрешены только PDF файлы.";
        }
      }
    },
    isPdf(file) {
      return file.type === "application/pdf";
    },
    async uploadFile() {
      if (!this.file) {
        this.errorMessage = "Пожалуйста, выберите файл.";
        return;
      }

      const formData = new FormData();
      formData.append("pdf_file", this.file);

      this.loading = true;
      this.successMessage = "";
      this.errorMessage = "";

      try {
        const response = await api.post("/pdf", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        if (response.status === 200) {
          this.successMessage = "Файл успешно загружен!";
          this.file = null;
          this.$refs.fileInput.value = "";
        } else {
          this.errorMessage = "Ошибка при загрузке файла.";
        }
      } catch (error) {
        console.error("Ошибка при загрузке файла:", error);
        if (error.response && error.response.data && error.response.data.detail) {
          this.errorMessage = error.response.data.detail;
        } else {
          this.errorMessage = "Ошибка при загрузке файла.";
        }
      } finally {
        this.loading = false;
      }
    },
    async fetchStatus() {
      try {
        const response = await api.get("/pdf");
        if (response.status === 200 && response.data.status) {
          this.status = response.data.status;
        } else {
          this.status = "";
          this.errorMessage = "Не удалось получить статус.";
        }
      } catch (error) {
        console.error("Ошибка при получении статуса:", error);
        this.errorMessage = "Ошибка при получении статуса.";
      } finally {
        this.isStatusLoading = false;
      }
    },
    startPolling() {
      this.pollInterval = setInterval(this.fetchStatus, 5000);
    },
    stopPolling() {
      if (this.pollInterval) {
        clearInterval(this.pollInterval);
        this.pollInterval = null;
      }
    },
  },
  created() {
    this.fetchStatus();
    this.startPolling();
  },
  beforeUnmount() {
    this.stopPolling();
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

.disabled-dropzone {
  cursor: not-allowed;
  opacity: 0.6;
}
</style>
