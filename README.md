# turinglab-elmasasya

## Proje Hakkında
TuringLab, Hesaplama Kuramı dersi final ödevi kapsamında geliştirilen,
deterministic single-tape Turing makinelerini simüle eden bir Python kütüphanesidir.

## Ödev Bilgileri
- **Ders:** Hesaplama Kuramı — Bilgisayar Mühendisliği
- **Başlangıç:** 4 Mayıs 2026
- **Son Teslim:** 22 Mayıs 2026, 23:59
- **Hazırlayan:** Dr. Ali Çetinkaya — Selçuk Üniversitesi
- **Değerlendiren:** Ahmet Erharman

[Open TuringLab Student Handbook](./TuringLab_Ogrenci_ElKitabi.pdf)

## Kullanım Örneği

```python
from turinglab import SingleTapeTM

tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")

result = tm.run(
    input_string="1011",
    max_steps=1000,
    verbose=True
)

print(result.accepted)
print(result.reason)
print(result.final_tape)
```

---

## Kafa Pozisyonu Politikası

Bu projede şerit yapısı dictionary tabanlı sparse tape olarak temsil edilmiştir.
Bu nedenle negatif kafa pozisyonlarına izin verilmektedir.
Kafa 0 pozisyonundan sola geçtiğinde -1, -2 gibi konumlarda çalışmaya devam edebilir.
