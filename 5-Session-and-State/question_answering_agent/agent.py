# Google ADK (Agent Development Kit) kütüphanesinden
# bir ajanın temel planını (blueprint) oluşturan ana 'Agent' sınıfını içe aktar.
from google.adk.agents import Agent

# Sistemin ana "beynini" (kök ajanı) oluştur
# 'Agent' sınıfından yeni bir örnek (nesne) oluşturuyoruz.
# Bu, bizim soru-cevap botumuzun kendisi olacak.
question_answering_agent = Agent(
    
    # 'name': Ajana verdiğimiz kimlik adı. 
    # Loglama (kayıt tutma) ve hata ayıklama (debugging) için kullanılır.
    name="question_answering_agent",
    
    # 'model': Ajanın düşünmek ve cevap üretmek için kullanacağı 
    # Temel Dil Modeli (LLM). Burada "gemini-2.0-flash" kullanılıyor,
    # bu model hızlı yanıtlar için optimize edilmiştir.
    model="gemini-2.0-flash",
    
    # 'description': Bu ajanın ne iş yaptığını açıklayan kısa bir metin.
    # Özellikle birden fazla ajanın olduğu karmaşık sistemlerde kullanışlıdır.
    description="Question answering agent",
    
    # 'instruction': Ajanın sistem talimatı (system prompt).
    # Bu, ajanın kimliğini, rolünü ve nasıl davranması gerektiğini belirleyen
    # en önemli kısımdır. Üç tırnak (""") ile çok satırlı bir metin olarak tanımlanır.
    instruction="""
    You are a helpful assistant that answers questions about the user's preferences.

    Here is some information about the user:
    Name: 
    {user_name}
    Preferences: 
    {user_preferences}
    """,
    # YUKARIDAKİ TALİMATIN AÇIKLAMASI:
    # 1. Rol Tanımı: "You are a helpful assistant..." diyerek ajanın rolünü belirliyoruz.
    # 2. Yer Tutucular (Placeholders): {user_name} ve {user_preferences} alanları
    #    dinamik verilerin geleceği yerlerdir.
    #
    # 3. Nasıl Çalışır?: Diğer kod dosyasındaki 'Runner', bu ajanı çalıştırdığında,
    #    önce 'session_service' (hafıza) içerisinden o anki oturumun (session) 
    #    durumunu (state) alır.
    #    Ardından, hafızadaki 'user_name' ve 'user_preferences' anahtarlarına karşılık 
    #    gelen değerleri (örn: "Brandon Hancock" ve "Pickleball sever...")
    #    otomatik olarak bu süslü parantezlerin içine yerleştirir.
    #    Böylece model, kullanıcıya özel bu bilgiyle donatılmış olarak soruyu yanıtlar.
)