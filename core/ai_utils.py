import google.generativeai as genai
import os

def analiz_et_gemini(seans_notlari_metni):
    # API Key'i o gizli kasadan (.env) çekiyoruz
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    if not GEMINI_API_KEY:
        return "Sistem Hatası: Gemini API Anahtarı bulunamadı."
        
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Sibel Hanım'ın asistanı için hazırladığımız özel komut (İsimsiz ve gizli)
    prompt = f"""
    Sen uzman bir klinik psikolog asistanısın. Aşağıda bir danışana ait geçmiş seans notları kronolojik olarak (isimler maskelenerek) verilmiştir.
    Lütfen bu notları analiz et, danışanın duygu durumundaki değişimleri, terapideki ilerlemeyi ve odaklanılması gereken temel sorunları profesyonel, klinik bir dille özetle.
    Bu özeti danışanın 'Genel Değerlendirme' dosyasına kaydedeceğiz. 
    
    Seans Notları:
    {seans_notlari_metni}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Yapay Zeka Analiz Hatası: {str(e)}"