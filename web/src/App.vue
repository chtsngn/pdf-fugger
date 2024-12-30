<template>
  <main class="min-h-screen w-full bg-gray-100">
    <!-- Global Dropzone Overlay -->
    <div
      v-if="isDragging"
      class="fixed inset-0 z-50 bg-blue-500 bg-opacity-20 backdrop-blur-sm flex items-center justify-center"
      @dragover.prevent
      @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
    >
      <div class="bg-white p-8 rounded-lg shadow-xl text-center">
        <svg
          class="w-16 h-16 mx-auto mb-4 text-blue-500"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
          />
        </svg>
        <h2 class="text-xl font-semibold text-gray-800 mb-2">PDF'i Buraya Bırakın</h2>
        <p class="text-gray-600">İşleme otomatik olarak başlayacak</p>
      </div>
    </div>

    <!-- Fullscreen Modal -->
    <div v-if="fullscreenPdf" class="fixed inset-0 z-50 bg-black bg-opacity-75 flex items-center justify-center">
      <div class="w-full h-full p-4">
        <div class="relative w-full h-full">
          <button
            @click="closeFullscreen"
            class="absolute top-4 right-4 bg-white rounded-full p-2 hover:bg-gray-100 transition-colors duration-200"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <iframe
            :src="fullscreenPdf"
            class="w-full h-full rounded-lg"
            title="PDF Önizleme"
          ></iframe>
        </div>
      </div>
    </div>

    <!-- Toast Bildirimi -->
    <div
      v-if="showToast"
      class="fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg flex items-center space-x-2 transition-all duration-300 transform translate-y-0 opacity-100"
      :class="{ 'translate-y-12 opacity-0': !showToast }"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
      </svg>
      <span>PDF başarıyla işlendi!</span>
    </div>

    <div
      @dragenter.prevent="handleDragEnter"
      @dragover.prevent
      class="min-h-screen w-full"
    >
      <div class="container mx-auto px-4 py-8">
        <div class="max-w-4xl mx-auto">
          <h1 class="text-3xl font-bold text-center mb-8 text-gray-800">
            PDFugger
          </h1>
          
          <div class="bg-white p-8 rounded-lg shadow-lg">
            <div class="flex flex-col items-center justify-center w-full space-y-6">
              <!-- Filtre Ayarları -->
              <div class="w-full border-2 border-gray-300 rounded-lg">
                <div class="flex items-center justify-between cursor-pointer p-2 transition-all duration-300 overflow-hidden hover:bg-gray-100 rounded-lg align-center" @click="isFiltersOpen = !isFiltersOpen">
                  <h3 class="text-lg font-semibold text-gray-700">Filtre Ayarları</h3>
                  <button class="text-gray-500 hover:text-gray-700 transition-colors duration-200">
                    <svg 
                      class="w-6 h-6 transform transition-transform duration-200"
                      :class="{ 'rotate-180': isFiltersOpen }"
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                </div>
                
                <div 
                  class="space-y-4 transition-all duration-300 overflow-hidden"
                  :class="{ 'h-0 opacity-0': !isFiltersOpen, 'h-auto opacity-100 p-2': isFiltersOpen }"
                >
                  <!-- Mürekkep Lekesi Slider -->
                  <div class="space-y-2">
                    <div class="flex justify-between">
                      <label class="text-sm text-gray-600">Mürekkep Lekesi Yoğunluğu</label>
                      <span class="text-sm text-gray-500">{{ ((inkSpots - 0.99) * 10000).toFixed(1) }}%</span>
                    </div>
                    <input
                      type="range"
                      v-model="inkSpots"
                      min="0.99"
                      max="0.9999"
                      step="0.0001"
                      class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                    />
                  </div>

                  <!-- Bulanıklık Slider -->
                  <div class="space-y-2">
                    <div class="flex justify-between">
                      <label class="text-sm text-gray-600">Bulanıklık Seviyesi</label>
                      <span class="text-sm text-gray-500">{{ (blurRadius * 100).toFixed(1) }}%</span>
                    </div>
                    <input
                      type="range"
                      v-model="blurRadius"
                      min="0"
                      max="2"
                      step="0.1"
                      class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                    />
                  </div>

                  <!-- Solukluk Slider -->
                  <div class="space-y-2">
                    <div class="flex justify-between">
                      <label class="text-sm text-gray-600">Yazı Solukluğu</label>
                      <span class="text-sm text-gray-500">{{ ((fadeLevel - 1) * 100).toFixed(1) }}%</span>
                    </div>
                    <input
                      type="range"
                      v-model="fadeLevel"
                      min="1"
                      max="1.5"
                      step="0.01"
                      class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                    />
                  </div>
                </div>
              </div>

              <!-- Dosya Seçme Alanı -->
              <label
                for="dropzone-file"
                :class="`flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-lg cursor-pointer transition-colors duration-200 ease-in-out
                  ${loading ? 'bg-gray-100 border-gray-300' : 'border-gray-400 hover:bg-gray-50'}`"
              >
                <div class="flex flex-col items-center justify-center pt-5 pb-6 px-4">
                  <svg
                    class="w-8 h-8 mb-3 text-gray-500"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                    />
                  </svg>
                  <template v-if="selectedFile">
                    <p class="mb-2 text-sm text-gray-600">
                      <span class="font-semibold">{{ selectedFile.name }}</span>
                    </p>
                    <p class="text-xs text-gray-500">Değiştirmek için tıklayın</p>
                  </template>
                  <template v-else>
                    <p class="mb-2 text-sm text-gray-600">
                      <span class="font-semibold">PDF yüklemek için tıklayın</span>
                    </p>
                    <p class="text-xs text-gray-500">veya sürükleyip bırakın</p>
                  </template>
                </div>
                <input
                  id="dropzone-file"
                  type="file"
                  class="hidden"
                  accept=".pdf"
                  @change="handleFileSelect"
                  :disabled="loading"
                />
              </label>

              <!-- Progress Bar -->
              <div v-if="loading" class="w-full space-y-2">
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                  <div class="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
                       :style="{ width: `${progress}%` }"></div>
                </div>
                <p class="text-sm text-center text-gray-600">İşleniyor... {{ progress.toFixed(1) }}%</p>
              </div>

              <!-- Yükleme Butonu -->
              <button
                v-if="selectedFile && !loading"
                @click="handleFileUpload"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 disabled:opacity-50"
                :disabled="loading"
              >
                Yükle ve İşle
              </button>

              <!-- PDF Önizleme -->
              <div v-if="selectedFile || processedFileUrl" class="w-full grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Orijinal PDF -->
                <div v-if="selectedFile" class="space-y-2">
                  <div class="flex items-center justify-between">
                    <h3 class="font-semibold text-gray-700">Orijinal PDF</h3>
                    <button
                      @click="openFullscreen(originalFileUrl)"
                      class="text-blue-600 hover:text-blue-700 text-sm flex items-center"
                    >
                      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                      </svg>
                      Tam Ekran
                    </button>
                  </div>
                  <div class="border rounded-lg p-4 bg-gray-50">
                    <iframe
                      :src="originalFileUrl"
                      class="w-full h-[500px] border-0"
                      title="Orijinal PDF"
                    ></iframe>
                  </div>
                </div>

                <!-- İşlenmiş PDF -->
                <div v-if="processedFileUrl" class="space-y-2">
                  <div class="flex items-center justify-between">
                    <h3 class="font-semibold text-gray-700">İşlenmiş PDF</h3>
                    <div class="flex items-center space-x-2">
                      <button
                        @click="downloadFile"
                        class="bg-green-600 text-white px-4 py-1 rounded-md text-sm flex items-center"
                      >
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                        </svg>
                        İndir
                      </button>
                      <div class="w-px h-4 bg-gray-300"></div>
                      <button
                        @click="openFullscreen(processedFileUrl)"
                        class="text-blue-600 hover:text-blue-700 text-sm flex items-center"
                      >
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                        </svg>
                        Tam Ekran
                      </button>
                    </div>
                  </div>
                  <div class="border rounded-lg p-4 bg-gray-50">
                    <iframe
                      :src="processedFileUrl"
                      class="w-full h-[500px] border-0"
                      title="İşlenmiş PDF"
                    ></iframe>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'

const loading = ref(false)
const progress = ref(0)
const selectedFile = ref<File | null>(null)
const processedFileUrl = ref<string | null>(null)
const fullscreenPdf = ref<string | null>(null)
const showToast = ref(false)
const isFiltersOpen = ref(true)
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001'

// Filtre parametreleri
const inkSpots = ref(0.9901)
const blurRadius = ref(0.8)
const fadeLevel = ref(1.25)

const isDragging = ref(false)
let dragCounter = 0

// LocalStorage'dan parametreleri yükle
onMounted(() => {
  const savedParams = localStorage.getItem('filterParams')
  if (savedParams) {
    const params = JSON.parse(savedParams)
    inkSpots.value = params.inkSpots
    blurRadius.value = params.blurRadius
    fadeLevel.value = params.fadeLevel
    isFiltersOpen.value = params.isFiltersOpen
  }

  // Dragleave event'ini dinle
  document.addEventListener('dragleave', (e) => {
    if (e.clientX === 0 || e.clientY === 0) {
      isDragging.value = false
      dragCounter = 0
    }
  })

  // Drop event'ini engelle
  document.addEventListener('drop', (e) => {
    e.preventDefault()
  })
})

// Parametreleri localStorage'a kaydet
watch([inkSpots, blurRadius, fadeLevel, isFiltersOpen], () => {
  localStorage.setItem('filterParams', JSON.stringify({
    inkSpots: inkSpots.value,
    blurRadius: blurRadius.value,
    fadeLevel: fadeLevel.value,
    isFiltersOpen: isFiltersOpen.value
  }))
}, { deep: true })

// Orijinal PDF için URL
const originalFileUrl = computed(() => {
  if (!selectedFile.value) return undefined
  return URL.createObjectURL(selectedFile.value)
})

const openFullscreen = (url: string | undefined) => {
  if (url) {
    fullscreenPdf.value = url
  }
}

const closeFullscreen = () => {
  fullscreenPdf.value = null
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    selectedFile.value = file
    processedFileUrl.value = null
  }
}

const simulateProgress = () => {
  progress.value = 0
  const interval = setInterval(() => {
    if (progress.value < 90) {
      progress.value += Math.random() * 10
    }
    if (!loading.value) {
      clearInterval(interval)
      progress.value = 100
    }
  }, 500)
}

// Toast gösterme fonksiyonu
const showSuccessToast = () => {
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000) // 3 saniye sonra kaybolur
}

const handleFileUpload = async () => {
  if (!selectedFile.value) return

  try {
    loading.value = true
    simulateProgress()
    
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('ink_spots', inkSpots.value.toString())
    formData.append('blur_radius', blurRadius.value.toString())
    formData.append('fade_level', fadeLevel.value.toString())

    const response = await fetch(`${API_URL}/process-pdf`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      throw new Error('PDF işleme hatası')
    }

    const blob = await response.blob()
    processedFileUrl.value = URL.createObjectURL(blob)
    progress.value = 100
    showSuccessToast() // İşlem başarılı olduğunda toast göster
  } catch (error) {
    console.error('Hata:', error)
    alert('PDF işlenirken bir hata oluştu')
  } finally {
    loading.value = false
  }
}

const downloadFile = () => {
  if (!processedFileUrl.value) return

  const a = document.createElement('a')
  a.href = processedFileUrl.value
  a.download = 'processed.pdf'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}

const handleDragEnter = (e: DragEvent) => {
  e.preventDefault()
  dragCounter++
  if (dragCounter === 1) {
    isDragging.value = true
  }
}

const handleDrop = async (e: DragEvent) => {
  e.preventDefault()
  isDragging.value = false
  dragCounter = 0

  const files = e.dataTransfer?.files
  if (!files || files.length === 0) return

  const file = files[0]
  if (!file.type.includes('pdf')) {
    alert('Lütfen sadece PDF dosyası yükleyin')
    return
  }

  selectedFile.value = file
  processedFileUrl.value = null
}
</script>
