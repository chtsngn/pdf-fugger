from PyPDF2 import PdfReader, PdfWriter
import io
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
Image.MAX_IMAGE_PIXELS = None  # Görüntü boyutu limitini kaldır
import pdf2image
import tempfile
import os
import random
import numpy as np

class PDFProcessor:
    def __init__(self):
        self.filters = []

    def add_noise(self, image, ink_spots=0.999):
        """Görüntüye rastgele gürültü ve mürekkep lekeleri ekler"""
        # Görüntüyü numpy dizisine çevir
        img_array = np.array(image)
        
        # Rastgele noktalar ekle (mürekkep lekeleri)
        noise = np.random.randint(0, 255, img_array.shape, dtype=np.uint8)
        # ink_spots değeri arttıkça daha fazla leke olacak
        mask = np.random.random(img_array.shape[:2]) < (ink_spots - 0.99)
        if len(img_array.shape) == 3:  # Renkli görüntü
            mask = np.stack([mask] * 3, axis=-1)
        img_array[mask] = noise[mask]
        
        # Görüntüyü PIL Image'e geri çevir
        noisy_image = Image.fromarray(img_array)
        return noisy_image

    def add_scan_effect(self, image, blur_radius=0.5, fade_level=1.15):
        """Taranmış görüntü efekti ekler"""
        # Hafif bulanıklaştırma
        blurred = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        
        # Kontrastı artır (daha az)
        enhancer = ImageEnhance.Contrast(blurred)
        contrasted = enhancer.enhance(1.1)
        
        # Keskinliği azalt
        sharpness = ImageEnhance.Sharpness(contrasted)
        less_sharp = sharpness.enhance(0.8)
        
        # Parlaklığı artır (yazıları soluklaştırmak için)
        brightness = ImageEnhance.Brightness(less_sharp)
        dimmed = brightness.enhance(fade_level)
        
        # Dikey siliklik efekti ekle
        width, height = dimmed.size
        img_array = np.array(dimmed)
        
        # Debug için çizim yapacak bir PIL Image oluştur
        debug_image = Image.fromarray(img_array)
        draw = ImageDraw.Draw(debug_image)
        
        # Görüntü genişliğine göre katlama aralığını ayarla
        base_interval = width // 8  # Sayfayı yaklaşık 8 parçaya böl
        fold_interval = base_interval + random.randint(-100, 100)  # Biraz rastgelelik ekle
        
        # Katlama pozisyonlarını hesapla
        fold_positions = []
        current_pos = fold_interval
        while current_pos < width:
            fold_positions.append(current_pos)
            current_pos += fold_interval + random.randint(-100, 100)
        
        for x in fold_positions:
            fold_width = random.randint(50, 60)
            start = max(0, x - fold_width // 2)
            end = min(width, x + fold_width // 2)
            
            # Debug için çerçeve çiz
            draw.rectangle([(start, 0), (end, height-1)], outline='red', width=5)
            
            # Tüm bölgeyi beyazlaştır (silikleştir)
            if len(img_array.shape) == 3:  # RGB görüntü için
                img_array[:, start:end, :] = img_array[:, start:end, :] * 0.3 + 255 * 0.7
            else:  # Gri tonlamalı görüntü için
                img_array[:, start:end] = img_array[:, start:end] * 0.3 + 255 * 0.7
            
            # Kenarları yumuşat
            blend_width = 2  # Yumuşatma genişliği
            
            # Sol kenar yumuşatma
            for i in range(blend_width):
                blend_factor = i / blend_width
                pos = start + i
                if pos < width:
                    if len(img_array.shape) == 3:
                        img_array[:, pos, :] = img_array[:, pos, :] * blend_factor + \
                                             (img_array[:, pos, :] * 0.3 + 255 * 0.7) * (1 - blend_factor)
                    else:
                        img_array[:, pos] = img_array[:, pos] * blend_factor + \
                                          (img_array[:, pos] * 0.3 + 255 * 0.7) * (1 - blend_factor)
            
            # Sağ kenar yumuşatma
            for i in range(blend_width):
                blend_factor = i / blend_width
                pos = end - i
                if pos >= 0:
                    if len(img_array.shape) == 3:
                        img_array[:, pos, :] = img_array[:, pos, :] * blend_factor + \
                                             (img_array[:, pos, :] * 0.3 + 255 * 0.7) * (1 - blend_factor)
                    else:
                        img_array[:, pos] = img_array[:, pos] * blend_factor + \
                                          (img_array[:, pos] * 0.3 + 255 * 0.7) * (1 - blend_factor)
        
        return Image.fromarray(img_array.astype(np.uint8))

    def add_paper_texture(self, image):
        """Kağıt dokusu ve kırışıklık efekti ekler"""
        # Orijinal boyutları al
        width, height = image.size
        
        # Yeni bir katman oluştur
        texture = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(texture)
        
        # Rastgele çizgiler ekle (kağıt kırışıklıkları)
        for _ in range(30):  # Çizgi sayısını azalttık
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = x1 + random.randint(-100, 100)
            y2 = y1 + random.randint(-100, 100)
            draw.line([(x1, y1), (x2, y2)], fill=(128, 128, 128, 5), width=1)  # Daha soluk çizgiler
        
        # Texture'ı orijinal görüntüyle birleştir
        return Image.alpha_composite(image.convert('RGBA'), texture)

    def process_pdf(self, pdf_bytes, ink_spots=0.999, blur_radius=0.5, fade_level=1.15):
        """PDF'i işler ve sonucu bytes olarak döner"""
        # Geçici dosya oluştur
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_input_file:
            temp_input_file.write(pdf_bytes)
            temp_input_path = temp_input_file.name

        try:
            # PDF'i görüntülere dönüştür
            images = pdf2image.convert_from_path(
                temp_input_path,
                thread_count=2,  # İş parçacığı sayısını sınırla
                grayscale=True,  # Direkt gri tonlama yap
                use_pdftocairo=True  # Daha hızlı dönüşüm için pdftocairo kullan
            )
            
            if not images:
                raise ValueError("PDF dosyası okunamadı veya boş")

            # Her sayfaya efektleri uygula
            processed_images = []
            for img in images:
                try:
                    # Tarama efektlerini uygula
                    img = self.add_scan_effect(img, blur_radius, fade_level)
                    img = self.add_noise(img, ink_spots)
                    
                    # RGBA'ya çevir ve kağıt dokusu ekle
                    img = img.convert('RGBA')
                    img = self.add_paper_texture(img)
                    
                    # Son olarak RGB'ye çevir (PDF için)
                    img = img.convert('RGB')
                    processed_images.append(img)
                except Exception as e:
                    print(f"Sayfa işlenirken hata: {str(e)}")
                    # Hata durumunda orijinal görüntüyü kullan
                    processed_images.append(img.convert('RGB'))
            
            # Görüntüleri yeni bir PDF'e dönüştür
            output_pdf_bytes = io.BytesIO()
            if processed_images:
                processed_images[0].save(
                    output_pdf_bytes,
                    save_all=True,
                    append_images=processed_images[1:],
                    format='PDF',
                    # optimize=True  # PDF boyutunu optimize et
                )
            
            output_pdf_bytes.seek(0)
            return output_pdf_bytes.getvalue()

        finally:
            # Geçici dosyayı temizle
            if os.path.exists(temp_input_path):
                os.remove(temp_input_path)

    def convert_to_grayscale(self, image):
        """Görüntüyü siyah-beyaz yapar"""
        return image.convert('L')

    def add_filter(self, filter_func):
        """Yeni bir filtre ekler"""
        self.filters.append(filter_func) 