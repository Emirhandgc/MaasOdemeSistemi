**Maaş Ödeme Sistemi:**
![SistemFoto](https://github.com/Emirhandgc/MaasOdemeSistemi/assets/76902278/f7f91249-3a88-4cdf-bd59-b9420b1dfb53)


Maaş Ödeme Sistemi, bir şirketin maaş ödemelerini yönetmek için kullanılan bir PyQt5 tabanlı bir uygulamadır. Bu sistem, şirketin bakiyesini yönetmek, 
çalışanları eklemek, çıkarmak veya düzenlemek, departmanlara maaş ödemek ve dekontları göndermek gibi temel işlevleri içerir.

**_Kullanım Kılavuzu:_**

Şirket Bakiyesi Görüntüleme ve Güncelleme:
"Şirket Bakiyesi" başlığı altında mevcut bakiyeyi görebilirsiniz.
"Bakiyeyi Güncelle" düğmesini kullanarak şirket bakiyesini güncelleyebilirsiniz. Yeni bakiyeyi girip düğmeye tıkladıktan sonra güncelleme işlemi gerçekleştirilir.

**_Departman Seçimi:_**
"Departman" başlığı altında mevcut departmanları seçebilirsiniz.
Departman seçimi değiştirildiğinde, o departmana ait çalışanlar otomatik olarak listelenir.

**_Çalışan İşlemleri:_**
"Çalışan Ekle" düğmesiyle yeni bir çalışan ekleyebilirsiniz. Ad, IBAN ve maaş ödeme tarihini girmeniz istenir.
"Çalışan Çıkar" düğmesiyle seçili çalışanı sistemden çıkarabilirsiniz.
"Çalışan Bilgilerini Düzenle" düğmesiyle seçili çalışanın bilgilerini düzenleyebilirsiniz.

**_Maaş Ödeme İşlemleri:_**
"Maaş Öde" düğmesiyle seçili departmana maaş ödemesi yapabilirsiniz. Şirket bakiyesi yeterli değilse uyarı alırsınız.
Maaş ödemesi yapıldıktan sonra, "Dekont Gönder" düğmesi aktif hale gelir. Bu düğmeye tıklayarak dekontları gönderebilirsiniz.

**_Gelecek Güncellemeler:_**
"Bakiye Güncelleme" butonuna tıklandığında doğrulama kodu isteyecek.
"Dekont Gönder" butonuna tıklandığında kime gönderileceğini ve ekstra belirtmek istenenleri bildirim ekranında gösterecek.
"Çalışan Ekle" butonuna tıklayıp girilen çalışan bilgileri boş bırakılamayacak.
Bütün departmanlarda çalışanları görüntüleyebilecek "Hepsi" bölümü seçenek olarak sunulacak.

