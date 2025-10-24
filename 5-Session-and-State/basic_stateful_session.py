# Gerekli kütüphaneleri ve modülleri içe aktar
import uuid  # Benzersiz (unique) kimlikler (ID) oluşturmak için kullanılır (örn: SESSION_ID)

from dotenv import load_dotenv  # .env dosyasındaki ortam değişkenlerini (örn: API anahtarı) yüklemek için
from google.adk.runners import Runner  # ADK'nın 'Runner' (Çalıştırıcı) sınıfı. Ajan ve oturum hizmetini birbirine bağlar.
from google.adk.sessions import InMemorySessionService  # Oturum (session) verilerini RAM'de (hafızada) tutan hizmet.
from google.genai import types  # 'Content' (İçerik) ve 'Part' (Bölüm) gibi standart mesaj yapıları için
from question_answering_agent.agent import question_answering_agent   # Ayrı bir dosyada tanımladığımız ajanın kendisi

# .env dosyasını bul ve içindeki değişkenleri (örn: GOOGLE_API_KEY) işletim sisteminin ortam değişkenlerine yükle
load_dotenv()


# --- 1. Oturum (Hafıza) Hizmetini Başlatma ---

# Oturum durumunu (state) programın çalıştığı süre boyunca RAM'de saklayacak
# yeni bir oturum hizmeti nesnesi oluştur.
session_service_stateful = InMemorySessionService()

# --- 2. Başlangıç Durumunu (Hafıza) Tanımlama ---

# Ajana daha en başta vermek istediğimiz bilgileri bir Python sözlüğü (dictionary) olarak tanımla.
# Bu, ajanın "hafızasını" oluşturur.
initial_state = {
    "user_name": "Brandon Hancock",  # Hafızaya 'user_name' anahtarını ekle
    "user_preferences": """
        I like to play Pickleball, Disc Golf, and Tennis.
        My favorite food is Mexican.
        My favorite TV show is Game of Thrones.
        Loves it when people like and subscribe to his YouTube channel.
    """,  # Hafızaya 'user_preferences' anahtarını (çok satırlı metinle) ekle
}

# --- 3. Yeni Bir Oturum (Session) Oluşturma ---

# Bu sohbet oturumunu tanımlayacak sabit bilgileri ayarla
APP_NAME = "Brandon Bot"  # Uygulamanın adı (kayıtları/logları gruplamak için)
USER_ID = "brandon_hancock"  # Bu sohbeti yapan kullanıcının kimliği

# uuid.uuid4() kullanarak bu spesifik sohbet için rastgele ve benzersiz bir kimlik oluştur.
# Bu, aynı kullanıcının farklı zamanlardaki sohbetlerini ayırmayı sağlar.
SESSION_ID = str(uuid.uuid4())

# Oturum hizmetini (hafıza yöneticisi) kullanarak yeni bir oturum kaydı oluştur.
# Bu işlem, 'initial_state' verisini alır ve 'SESSION_ID' ile ilişkilendirip hafızaya kaydeder.
stateful_session = session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,  # Hafızaya yüklenecek başlangıç verisi
)

# Kullanıcıya oturumun başarıyla oluşturulduğunu ve ID'sini bildir
print("CREATED NEW SESSION:")
print(f"\tSession ID: {SESSION_ID}")

# --- 4. Çalıştırıcıyı (Runner) Yapılandırma ---

# Runner, tüm süreci yöneten ana orkestratördür.
runner = Runner(
    agent=question_answering_agent,      # Bu Runner'ın hangi ajanı (beyni) kullanacağını belirt
    app_name=APP_NAME,                    # Runner'ın hangi uygulama adına ait olduğunu belirt
    session_service=session_service_stateful, # Bu Runner'ın hangi hafıza hizmetini kullanacağını belirt
)

# --- 5. Kullanıcının Mesajını Hazırlama ---

# Kullanıcıdan gelen soruyu ADK'nın anlayacağı standart 'Content' formatına dönüştür
new_message = types.Content(
    role="user",  # Mesajın sahibinin "kullanıcı" olduğunu belirt
    parts=[types.Part(text="What is Brandon's favorite food ?")]  # Mesajın metin içeriği
)

# --- 6. Ajanı Çalıştırma ve Yanıt Alma ---

# 'runner.run()' fonksiyonunu çağırarak tüm süreci başlat.
# Bu fonksiyon, ajanın düşünme adımları da dahil olmak üzere bir olay akışı (event stream) döndürür.
for event in runner.run(
    user_id=USER_ID,          # Hangi kullanıcı için çalıştırılacak
    session_id=SESSION_ID,    # Hangi oturum (hafıza) kullanılacak
    new_message=new_message,  # Kullanıcının yeni sorusu nedir
):     
    # Dönen olay akışındaki her bir 'event'i kontrol et
    # Eğer bu olay, ajanın verdiği "nihai cevap" ise...
    if event.is_final_response():
        # ...ve bu cevabın bir içeriği varsa...
        if event.content and event.content.parts:
            # ...bu içeriğin ilk metin bölümünü al ve ekrana yazdır.
            print(f"Final Response: {event.content.parts[0].text}")

# --- 7. Oturumun Son Durumunu Kontrol Etme ---

# (Bu bölüm, hafızanın değişip değişmediğini görmek için yapılan bir doğrulamadır)

# Sadece bilgi amaçlı olarak "==== Session Event Exploration ====" başlığını yazdır
print("==== Session Event Exploration ====")

# Oturum hizmetine git ve bu sohbete (SESSION_ID) ait hafızanın
# GÜNCEL durumunu (state) tekrar al.
session = session_service_stateful.get_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
)

# Hafızanın son durumunu ekrana yazdırmak için bir başlık yazdır
print("=== Final Session State ===")

# Alınan 'session' nesnesinin 'state' (durum) sözlüğü içindeki
# her bir anahtar (key) ve değeri (value) döngüye al
for key, value in session.state.items():
    # Anahtar ve değeri ekrana güzel bir formatta yazdır (örn: "user_name: Brandon Hancock")
    print(f"{key}: {value}")