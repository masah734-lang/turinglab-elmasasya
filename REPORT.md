# TuringLab Mini-Raporu

# 1. Giriş

Bu projede Python kullanarak deterministik tek şeritli bir Turing makinesi simülatörü geliştirdik. Projenin amacı derste gördüğümüz Turing makinelerini teorik olmaktan çıkarıp gerçek bir program üzerinde çalıştırabilmekti.

Projede makineler YAML dosyaları ile tanımlandı. Python tarafında ise bu dosyalar okunarak çalıştırıldı. Böylece farklı problemler için yazılan Turing makineleri aynı sistem üzerinde test edilebildi.

TuringLab temel olarak bir TM engine mantığında çalışmaktadır. Kullanıcı bir YAML dosyası verdiğinde program bu dosyayı okuyup durumları, geçişleri ve giriş alfabesini yüklemektedir. Daha sonra makine adım adım çalıştırılmaktadır.

Projede özellikle Turing makinelerinin çalışma mantığını daha iyi anlamış oldum. Derste teorik olarak görülen “state”, “transition”, “tape” gibi kavramların gerçek bir sistemde nasıl çalıştığını görmek öğretici oldu.

Başta özellikle kafa hareketleri ve transition yazımı biraz karıştırıcı geldi. Bazı makinelerde sonsuz döngü problemleri yaşandı. Ancak debug yaparak ve verbose çıktıları inceleyerek bu sorunlar çözüldü.

Proje sonunda çalışan bir TM engine, farklı örnek makineler ve pytest testleri elde edildi.

---

# 2. Mimari ve Tasarım Kararları

Projede ana dosya `tm_engine.py` dosyasıdır. Burada Turing makinesinin çalışmasını sağlayan temel yapılar bulunmaktadır.

Projede kullanılan temel sınıflar:

* Tape
* SingleTapeTM
* Configuration
* RunResult

`Tape` sınıfı Turing makinesinin şeridini temsil etmektedir.
`SingleTapeTM` ise YAML dosyasından makineyi okuyup çalıştırmaktadır.

Şerit yapısını tasarlarken liste yerine dictionary kullanmayı tercih ettik. Bunun temel nedeni Turing makinesinde şeridin teorik olarak sonsuz olmasıdır. Eğer liste kullansaydık özellikle sola doğru genişleyen durumlarda daha fazla kontrol yapmak gerekecekti.

Dictionary yapısında ise sadece kullanılan hücreler bellekte tutulmaktadır. Yazılmamış hücreler otomatik olarak blank sembolü döndürmektedir. Bu yöntem hem daha esnek hem de teorik TM modeline daha yakın oldu.

Geçiş fonksiyonları Python tarafında `(state, symbol)` mantığında tutuldu. Böylece mevcut durum ve okunan sembole göre yeni geçiş hızlı şekilde bulunabilmektedir.

Makinede dört farklı sonuç oluşabilmektedir:

* accept
* reject
* timeout
* no_transition

Eğer geçiş bulunamazsa makine durmaktadır. Kabul durumuna giderse accept sonucu dönmektedir.

Projede verbose modu da bulunmaktadır. Bu mod sayesinde her adım terminalde görülebilmektedir. Özellikle debug sırasında çok yardımcı oldu çünkü makinenin hangi durumda takıldığını görmek kolaylaştı.

Kod yapısı modüler tutulmaya çalışıldı. Böylece yeni bir Turing makinesi eklemek için sadece yeni bir YAML dosyası yazmak yeterli olmaktadır.

---

# 3. Tasarlanan Turing Makineleri

Projede farklı amaçlar için birkaç farklı Turing makinesi tasarlandı.

İlk olarak `binary_increment` makinesi binary sayı sistemindeki bir sayıyı 1 artırmaktadır. Örneğin `1011` girdisini `1100` yapmaktadır. Bu makinede binary toplama mantığı kullanılmıştır.

`unary_increment` makinesi unary sistemde verilen sayıyı bir artırmaktadır. Unary sistemde sayı tekrar eden `1` karakterleri ile gösterildiği için makine sadece sona yeni bir `1` eklemektedir.

`even_a` makinesi ise girdideki `a` karakteri sayısının çift olup olmadığını kontrol etmektedir. Makine çift ve tek durumları arasında geçiş yaparak çalışmaktadır.

`string_copy` makinesi verilen stringi kopyalamaktadır. Örneğin `abba` girdisini `abba#abba` haline getirmektedir. Bu makinede karakterlerin işaretlenmesi ve geri dönülmesi gerektiği için biraz daha karmaşık bir yapı oluştu.

Bence projedeki en zor makine `unary_to_binary` makinesi oldu. Çünkü bu makine sadece kabul veya red kararı vermiyor, aynı zamanda çıktı da üretiyor.

Unary kısımdaki her `1` karakteri için binary taraftaki sayacın artırılması gerekiyordu. Özellikle carry (elde) durumlarında birkaç kez sonsuz döngü problemi yaşandı. Debug yaparak ve binary increment mantığını ayrı düşünerek sorun çözüldü.

Genel olarak makineleri tasarlarken en zor kısım transitionları eksiksiz yazmak oldu. Küçük bir eksiklik bile makinenin yanlış çalışmasına veya sonsuz döngüye girmesine neden olabiliyordu.

---

# 4. Kavramsal Tartışma: Python ile Turing Makinesi Arasındaki Boşluk

Turing makineleri teorik bir hesaplama modelidir. Python gibi modern programlama dilleri ise gerçek dünyadaki problemlerin çözümü için geliştirilmiştir. Bu nedenle aralarında önemli farklar bulunmaktadır.

Turing makinesi çok basit bir yapıya sahiptir. Sadece bir şerit, bir kafa ve geçiş fonksiyonlarından oluşmaktadır. Bütün işlemler sembol okuma, yazma ve sağ-sol hareketleri ile yapılmaktadır.

Python ise bunun tam tersine oldukça yüksek seviyeli bir programlama dilidir. Hazır veri yapıları, fonksiyonlar, kütüphaneler ve otomatik bellek yönetimi gibi birçok özellik sunmaktadır.

Örneğin Python’da iki sayıyı toplamak tek satır sürerken, Turing makinesinde aynı işlem için onlarca transition yazılması gerekebilir. Bu durum modern diller ile teorik modeller arasındaki soyutlama farkını göstermektedir.

Ancak buna rağmen Turing makineleri bilgisayar biliminin temelini oluşturmaktadır. Çünkü modern programlama dillerinin teorik olarak yapabildiği her hesaplama bir Turing makinesi ile de yapılabilmektedir.

Bu projede özellikle basit görünen işlemlerin Turing makinesinde ne kadar detaylı hale geldiği görüldü. Örneğin binary increment işlemi Python’da çok kısa sürerken, TM tarafında kafa hareketleri, carry işlemleri ve state geçişleri tek tek tanımlanmak zorunda kaldı.

Bence projenin en öğretici kısmı buydu. Çünkü modern programlama dillerinin arka planda aslında ne kadar karmaşık işlemleri soyutladığını daha iyi anlamış oldum.

# 5. Sınırlar ve İleri Çalışma

Bu proje tek şeritli deterministik Turing makineleri için geliştirildiği için bazı gelişmiş özellikler eklenmedi.

Örneğin multi-tape veya non-deterministic TM desteği bulunmamaktadır. Ayrıca grafiksel bir arayüz yerine terminal çıktıları kullanılmıştır.

Bir hafta daha süre olsaydı görsel bir arayüz eklemek isterdik. Böylece state geçişleri ve şerit hareketleri daha rahat takip edilebilirdi.

Bunun dışında multi-tape desteği ve daha gelişmiş hata mesajları da eklenebilirdi.

Genel olarak proje temel hedeflerini başarılı şekilde gerçekleştirdi.

---

# 6. Kaynakça

* Ders notları ve TuringLab Öğrenci El Kitabı
* Michael Sipser — Introduction to the Theory of Computation
* Python resmi dokümantasyonu
* PyYAML dokümantasyonu
* pytest dokümantasyonu

