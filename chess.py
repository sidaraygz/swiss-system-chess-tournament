from math import ceil
from math import log2
from operator import itemgetter
from sys import exit

HATA = 'Aralığın dışında bir sayı girdiniz. Lütfen tekrar deneyin: '
HATA2 = 'Hata: Geçersiz bir sayı girdiniz.'
HIGHEST_POINT = 1
HALF_POINT = 0.5
ZERO_POINT = 0
MIN_ELO_AND_UKD = 1000


def get_number(text1):
    while True:
        try:
            number = int(input(text1))
            while 0 < number < MIN_ELO_AND_UKD or number < 0:
                number = int(input(HATA))
            break
        except ValueError:
            print(HATA2)
    return number


def unique_number(list1):
    while True:
        try:
            # lisans numarası alınır
            license_number = int(input('Oyuncunun lisans numarasını giriniz '
                                       '-başka bir oyuncu yoksa bitirmek için 0 ya da negatif girebilirsiniz- : '))
            # lisans numarası daha önce girilmişse tekrar istenir
            while license_number in [d['Lisans Numarası'] for d in list1]:
                print('Bu lisans numarası daha önce girildi. Lütfen tekrar deneyiniz.')
                license_number = int(
                    input('Oyuncunun lisans numarasını giriniz -bitirmek için 0 ya da negatif girebilirsiniz- : '))
            # lisans numarasının değeri döndürülür
            break
        except ValueError:
            print(HATA2)
    return license_number


# kullanıcıdan tur sayısını alan fonksiyon
def get_number_of_rounds(number2):
    while True:
        try:
            # verilen sayının 2 tabanına göre logaritması hesaplanıp yukarı doğru yuvarlanır
            log_round_number = ceil(log2(number2))
            number = int(
                input('Turnuvadaki tur sayisini giriniz ' + '(' + str(log_round_number) + '-' + str(number2 - 1) + ')'))
            while log_round_number > number or number > number2 - 1:
                number = int(input('Hatalı bir sayı girdiniz. Lütfen tekrar deneyin: '))
            break
        except ValueError:
            print(HATA2)
    return number


# verilen listeyi dökümandaki önceliğe göre sıralayan fonksiyon
def sort(list1):
    alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ "
    list1.sort(key=itemgetter('Lisans Numarası'))
    list1.sort(key=lambda name: [alphabet.index(c) for c in name['Ad-Soyad']])
    list1.sort(key=itemgetter('BH1', 'BH2', 'SB', 'GS', 'ELO', 'UKD', ), reverse=True)
    list1.sort(key=lambda x: x['Puan']['puan'], reverse=True)


# başlangıç sıralamasını yazdıran fonksiyon
def print_starting_table(list1):
    print('Başlangıç Sıralama Listesi:')
    print(f"{'BSNo':>4}", end='  ')
    print(f"{'LNo':>4}", end='  ')
    print(f"{'Ad-Soyad':>20}", end='  ')
    print(f"{'ELO':>4}", end='  ')
    print(f"{'UKD':>4}")
    print(f"{'----'}", end='  ')
    print(f"{'----'}", end='  ')
    print(f"{'--------------------'}", end='  ')
    print(f"{'----'}", end='  ')
    print(f"{'----'}")
    for i in range(len(list1)):
        list1[i]['BSNo'] = i + 1
        print(f"{list1[i]['BSNo']:>4}", end='  ')
        print(f"{list1[i]['Lisans Numarası']:>4}", end='  ')
        print(f"{list1[i]['Ad-Soyad']:>20}", end='  ')
        print(f"{list1[i]['ELO']:>4}", end='  ')
        print(f"{list1[i]['UKD']:>4}")


# kullanıcıdan ilk oyuncunun rengini alıp bu renge göre diğer oyunculara renk dağıtan fonksiyon
def get_and_give_colours(list1):
    # kullanıcdan ilk renk alınır
    first_colour = input('Başlangıç sıralamasına göre ilk oyuncunun ilk turdaki rengini giriniz (b/s): ').lower()
    while first_colour not in ['b', 's']:
        first_colour = input(HATA)
    # eğer listenin eleman sayısı çift basamaklı ise
    if len(list1) % 2 == 0:
        for i in range(len(list1)):
            # indexi çift olanlar ilk rengi alır
            if i % 2 == 0 and first_colour == 's':
                list1[i]['Renk'] = 's'
                list1[i]['s'] += 1
            elif i % 2 == 0 and first_colour == 'b':
                list1[i]['Renk'] = 'b'
                list1[i]['b'] += 1
            # indexi tek olanlar ilk rengin zıttını alır
            elif i % 2 != 0 and first_colour == 's':
                list1[i]['Renk'] = 'b'
                list1[i]['b'] += 1

            else:
                list1[i]['Renk'] = 's'
                list1[i]['s'] += 1
    # eğer listenin eleman sayısı tek basamaklı ise
    else:
        for i in range(len(list1)):
            # listenin sonundaki eleman bye geçeceğinden dolayı renk verilmez
            if list1[i] == list1[-1]:
                list1[i]['Renk'] = ''
                break
            # indexi çift olanlar ilk rengi alır
            if i % 2 == 0 and first_colour == 's':
                list1[i]['Renk'] = 's'
                list1[i]['s'] += 1
            elif i % 2 == 0 and first_colour == 'b':
                list1[i]['Renk'] = 'b'
                list1[i]['b'] += 1
            # indexi tek olanlar ilk rengin zıttını alır
            elif i % 2 != 0 and first_colour == 's':
                list1[i]['Renk'] = 'b'
                list1[i]['b'] += 1

            else:
                list1[i]['Renk'] = 's'
                list1[i]['s'] += 1


# oyunculara yeni renklerini veren fonksiyon
def give_new_colours(player, colour):
    # oyuncunun önceki iki rengi belirlenir
    player['O2R'][0] = player['Renk']
    # oyuncunun yeni rengi verilir
    player['Renk'] = colour
    player['O2R'][1] = colour
    if colour == 'b':
        # oyuncunun beyaz rengini alma sayısı 1 arttılır
        player['b'] += 1
    elif colour == 's':
        # oyuncunun siyah rengini alma sayısı 1 arttırılır
        player['s'] += 1


# iki oyuncuyu eşleştiren fonksiyon
def pair(player1, player2, match_list):
    # Önce beyaz ve siyah olarak sıralanır
    # Ardından eşleştirilir.
    match_list.append(sorted([player1, player2], key=lambda d: d["Renk"]))
    player1['Rakipler'].append(player2['BSNo'])
    player2['Rakipler'].append(player1['BSNo'])


def first_pairing(general_data_list, match_list, number_of_rounds):
    # 0'dan başlayıp ikişer artan bir for döngüsüne girilir
    for x in range(0, len(general_data_list), 2):
        # x ve x+1 indexli oyuncular eşleştirilmeye çalışılır
        try:
            pair(general_data_list[x], general_data_list[x + 1], match_list)
        # indexerror ile bye' geçecek olan oyuncu saptanır
        except IndexError:
            # maç listesinin başına bye geçen oyuncu eklenir
            match_list.insert(0, [general_data_list[-1], 'BYE'])
            # oyuncuları tutan veri listesinin son oyuncusu bye geçer
            # maç sonucu oyuncunun verilerine eklenir
            general_data_list[-1]['Maç Sonuçları'].append(['1', '-'])
            # eşleştirme bozarken kullanmak için bye geçen oyuncuya kurallara göre hayali bir rakip puanı eklenir
            general_data_list[-1]['Rakip Puanları'].append(
                {'puan': general_data_list[-1]['Puan']['puan'] + ((number_of_rounds - 1) * 0.5)})
            # çapraz tabloda gösterilmek üzere rakiplere - sembolü eklenir
            general_data_list[-1]['Rakipler'].append('-')


def reverse_colour(colour):
    if colour == 'b':
        return 's'
    elif colour == 's':
        return 'b'
    else:
        return ''


# oyuncuların bh puanlarını hesaplayan fonksiyon
def calculate_bh(general_data_list):
    # veri listesindeki her oyunucu dönen bir for döngüsü oluşturulur
    for x in general_data_list:
        # y puanlara göre sıralanmış bir listede döner en düşük puanı dönmez
        for y in sorted(x['Rakip Puanları'], key=itemgetter('puan'))[1:]:
            # puan kadar arttırlır
            x['BH1'] = x['BH1'] + y['puan']
        # y puanlara göre sıralanmış bir listede döner en düşük iki puanı dönmez
        for y in sorted(x['Rakip Puanları'], key=itemgetter('puan'))[2:]:
            # puan kadar arttırılır
            x['BH2'] = x['BH2'] + y['puan']


# oyuncuların sb puanını hesaplayan fonksiyon
def calculate_sb(general_data_list):
    # veri listesindeki her oyuncuyu dönen bir for döngüsü oluşturulur
    for x in general_data_list:
        # y maç sonuçlarında dönerken k rakip puanlarında döner
        for y, k in zip(x['Maç Sonuçları'], x['Rakip Puanları']):
            if y == ['1', '-'] or y == ['1', 'b'] or y == ['1', 's'] or y == ['+', 'b'] or y == ['+', 's']:
                # oyuncu galip gelmişse puanı kadar arttırılır
                x['SB'] += k['puan']
            elif y == ['½', 's'] or y == ['½', 'b']:
                # oyuncu berabere kaldıysa puanının yarısı kadar arttırılır
                x['SB'] += k['puan'] / 2


# oyuncuların gs puanlarını hesaplayan fonksiyon
def calculate_gs(general_data_list):
    for x in general_data_list:
        for y in x['Maç Sonuçları']:
            # oyuncunun oynayarak kazandığı veya rakibinin gelmediği maç sayısı hesaplanır
            if y == ['1', 's'] or y == ['+', 'b'] or y == ['+', 's'] or y == ['1', 'b']:
                x['GS'] += 1


def other_pairings(general_data_list, match_list, number_of_rounds, round_number):
    # eğer oyuncu sayısı tek sayısı ise sıralamada sondan başlanıp kurallara uyan ilk oyuncu bye geçer
    if len(general_data_list) % 2 != 0:
        for i in reversed(general_data_list):
            # kurallara uyulmuyorsa diğer oyuncuya bakılır
            if ['1', '-'] not in i['Maç Sonuçları'] and ['+', 's'] not in i['Maç Sonuçları'] and ['+', 'b'] not in i[
                'Maç Sonuçları']:
                # kurallara uyan bir oyuncu bulunduktan sonra maç listesinin başına bye ile eşleşerek eklenir
                match_list.append([i, 'BYE'])
                # çapraz tablo için gerekli semboller atanır
                i['Maç Sonuçları'].append(['1', '-'])
                # eşleştirme bozma fonksiyonlarında kullanılmak için hayali rakip puanı kurallara göre eklenir
                i['Rakip Puanları'].append(
                    {'puan': i['Puan']['puan'] + ((number_of_rounds - (round_number + 1)) * 0.5)})
                i['Rakipler'].append('-')
                # oyuncu bulunduktan sonra döngüden çıkılır
                break
    # bütün oyuncuları gezen bir for döngüsü oluşturulur
    for i in range(len(general_data_list)):
        # rakip aranan oyuncunun rengi bir değişkene atanır
        colour = general_data_list[i]['Renk']
        # rengin tersi bir değişkene atanır
        opposite_colour = reverse_colour(colour)
        # aranan puan aralığı bir değişkene atanır
        score_for_searching = general_data_list[i]['Puan']['puan']
        # oyuncu eşleşene kadar dönen bir while döngüsü oluşturulur
        while True:
            # rakip aranan oyuncu dışındaki oyuncuları gezen for döngüsü oluşturulur
            for j in range(i + 1, len(general_data_list)):
                # rakip oyuncunun rengi bir değişkene atanır
                opponent_colour = general_data_list[j]['Renk']
                reversed_opponent_colour = reverse_colour(opponent_colour)
                # dökümandaki 1.1 eşleşme kurallarına uyulursa ifin içine girilir ve eşleştirme yapılır
                if colour != opponent_colour and general_data_list[j]['BSNo'] not in general_data_list[i][
                    'Rakipler'] and \
                        general_data_list[
                            i] not in sum(match_list, []) and general_data_list[j] not in sum(match_list, []) and \
                        general_data_list[j]['Puan']['puan'] == score_for_searching:
                    # oyunculara yeni renkleri atanır

                    if general_data_list[i]['Renk'] == '':
                        if general_data_list[i][opponent_colour] - general_data_list[i][
                            reversed_opponent_colour] < 2 and general_data_list[j][reversed_opponent_colour] - \
                                general_data_list[j][opponent_colour] < 2:
                            give_new_colours(general_data_list[i], opponent_colour)
                            give_new_colours(general_data_list[j], reversed_opponent_colour)
                    else:
                        if general_data_list[i][opposite_colour] - general_data_list[i][colour] < 2 and \
                                general_data_list[j][colour] - general_data_list[j][opposite_colour] < 2:
                            give_new_colours(general_data_list[i], opposite_colour, )
                            give_new_colours(general_data_list[j], colour)
                    # oyuncular eşleştirilir
                    pair(general_data_list[i], general_data_list[j], match_list)
                    # iç döngüden çıkılır
                    break
            # oyuncunun eşleştirdiği kontrol edilir(i)
            if general_data_list[i] in sum(match_list, []):
                # oyuncu eşleştirilmişse diğer döngülere girmenin anlamı olmadığından while döngüsünden çıkılır(ii)
                break
            # oyuncu eşleşmemişse dökümanda 1.2 kurallarına bakılır
            for j in range(i + 1, len(general_data_list)):
                opponent_colour = general_data_list[j]['Renk']
                if colour == opponent_colour and general_data_list[j]['BSNo'] not in general_data_list[i][
                    'Rakipler'] and \
                        general_data_list[j]['O2R'] != [opponent_colour, opponent_colour] and general_data_list[
                    i] not in sum(match_list, []) and general_data_list[j] not in sum(match_list, []) and \
                        general_data_list[j]['Puan']['puan'] == score_for_searching and general_data_list[i][
                    opposite_colour] - general_data_list[i][opponent_colour] < 2 and general_data_list[j][
                    opponent_colour] - general_data_list[j][opposite_colour] < 2:
                    give_new_colours(general_data_list[i], opposite_colour)
                    give_new_colours(general_data_list[j], opponent_colour)
                    pair(general_data_list[i], general_data_list[j], match_list)
                    break
            # i
            if general_data_list[i] in sum(match_list, []):
                # ii
                break
            # oyuncu eşleşmemişse dökümanda 1.3 kurallarına bakılır
            for j in range(i + 1, len(general_data_list)):
                opponent_colour = general_data_list[j]['Renk']
                if colour == opponent_colour and general_data_list[j]['BSNo'] not in general_data_list[i][
                    'Rakipler'] and \
                        general_data_list[i]['O2R'] != [colour, colour] and general_data_list[
                    i] not in sum(match_list, []) and general_data_list[j] not in sum(match_list, []) and \
                        general_data_list[j]['Puan']['puan'] == score_for_searching and general_data_list[i][colour] - \
                        general_data_list[i][opposite_colour] < 2 and general_data_list[j][opposite_colour] - \
                        general_data_list[j][colour] < 2:
                    give_new_colours(general_data_list[i], colour)
                    give_new_colours(general_data_list[j], opposite_colour)
                    pair(general_data_list[i], general_data_list[j], match_list)
                    break
            # i
            if general_data_list[i] in sum(match_list, []):
                # ii
                break
            # oyuncular hala eşleştirilmemişse puan aralığı 0.5 kadar düşürülüp döngünün başına dönülür
            else:
                score_for_searching -= 0.5


def cross_table(general_data_list, number_of_rounds):
    print('Çapraz Tablo:')
    print(f"{'BSNo':>4}", end='  ')
    print(f"{'SNo':>3}", end='  ')
    print(f"{'LNo':>5}", end='  ')
    print(f"{'Ad-Soyad':>12}", end='  ')
    print(f"{'ELO':>4}", end='  ')
    print(f"{'UKD':>4}", end='  ')
    for x in range(number_of_rounds):
        print(f"{str(x + 1) + '. Tur':>7}", end='  ')
    print(f"{'Puan':>4}", end='  ')
    print(f"{'BH1':>5}", end='  ')
    print(f"{'BH2':>5}", end='  ')
    print(f"{'SB':>5}", end='  ')
    print(f"{'GS':>4}")
    print(f"{'----'}", end='  ')
    print(f"{'---'}", end='  ')
    print(f"{'-----'}", end='  ')
    print(f"{'------------'}", end='  ')
    print(f"{'----'}", end='  ')
    print(f"{'----'}", end='  ')
    for x in range(number_of_rounds):
        print(f"{'-------'}", end='  ')
    print(f"{'----'}", end='  ')
    print(f"{'-----'}", end='  ')
    print(f"{'-----'}", end='  ')
    print(f"{'-----'}", end='  ')
    print(f"{'----'}")
    general_data_list.sort(key=itemgetter('BSNo'))
    for x in range(len(general_data_list)):
        print(f"{general_data_list[x]['BSNo']:>4}", end='  ')
        print(f"{general_data_list[x]['SNo']:>3}", end='  ')
        print(f"{general_data_list[x]['Lisans Numarası']:>5}", end='  ')
        print(f"{general_data_list[x]['Ad-Soyad']:>12}", end='  ')
        print(f"{general_data_list[x]['ELO']:>4}", end='  ')
        print(f"{general_data_list[x]['UKD']:>4}", end='  ')
        for y, k in zip(general_data_list[x]['Maç Sonuçları'], general_data_list[x]['Rakipler']):
            print(f"{k:>3}", end=' ')
            print(f"{y[1]:>1}", end=' ')
            print(f"{y[0]:>1}", end='  ')
        print(f"{general_data_list[x]['Puan']['puan']:>4.2f}", end='  ')
        print(f"{general_data_list[x]['BH1']:>5.2f}", end='  ')
        print(f"{general_data_list[x]['BH2']:>5.2f}", end='  ')
        print(f"{general_data_list[x]['SB']:>5.2f}", end='  ')
        print(f"{general_data_list[x]['GS']:>4}")


def ultimate_ranking(general_data_list):
    print('Nihai Sıralama Listesi:')
    print(f"{'SNo':>3}", end='  ')
    print(f"{'BSNo':>4}", end='  ')
    print(f"{'LNo':>5}", end='  ')
    print(f"{'Ad-Soyad':>12}", end='  ')
    print(f"{'ELO':>4}", end='  ')
    print(f"{'UKD':>4}", end='  ')
    print(f"{'Puan':>4}", end='  ')
    print(f"{'BH1':>5}", end='  ')
    print(f"{'BH2':>5}", end='  ')
    print(f"{'SB':>5}", end='  ')
    print(f"{'GS':>4}")
    print(f"{'---'}", end='  ')
    print(f"{'----'}", end='  ')
    print(f"{'-----'}", end='  ')
    print(f"{'------------'}", end='  ')
    print(f"{'----'}", end='  ')
    print(f"{'----'}", end='  ')
    print(f"{'----'}", end='  ')
    print(f"{'-----'}", end='  ')
    print(f"{'-----'}", end='  ')
    print(f"{'-----'}", end='  ')
    print(f"{'----'}")
    for x in range(len(general_data_list)):
        general_data_list[x]['SNo'] = x + 1
        print(f"{general_data_list[x]['SNo']:>3}", end='  ')
        print(f"{general_data_list[x]['BSNo']:>4}", end='  ')
        print(f"{general_data_list[x]['Lisans Numarası']:>5}", end='  ')
        print(f"{general_data_list[x]['Ad-Soyad']:>12}", end='  ')
        print(f"{general_data_list[x]['ELO']:>4}", end='  ')
        print(f"{general_data_list[x]['UKD']:>4}", end='  ')
        print(f"{general_data_list[x]['Puan']['puan']:>4.2f}", end='  ')
        print(f"{general_data_list[x]['BH1']:>5,.2f}", end='  ')
        print(f"{general_data_list[x]['BH2']:>5.2f}", end='  ')
        print(f"{general_data_list[x]['SB']:>5.2f}", end='  ')
        print(f"{general_data_list[x]['GS']:>4}")


# eşleştirme tablosunun diğer yarısını yazdıran fonksiyon
def make_pair_table(match_list, general_data_list):
    # maç sayısı tek iken bye olacağından ona göre yazdılır
    if len(general_data_list) % 2 != 0:
        for table in range(1, len(match_list)):
            print(f"{table:>3}", end='  ')
            print(f"{match_list[table][0]['BSNo']:>4}", end='  ')
            print(f"{match_list[table][0]['Lisans Numarası']:>3}", end=' ')
            print(f"{match_list[table][0]['Puan']['puan']:>4.2f}", end='  ')
            print(f"{match_list[table][1]['Puan']['puan']:>8.2f}", end='  ')
            print(f"{match_list[table][1]['Lisans Numarası']:>3}", end='  ')
            print(f"{match_list[table][1]['BSNo']:>4}")
        print(f"{len(match_list):>3}", end='  ')
        print(f"{match_list[0][0]['BSNo']:>4}", end='  ')
        print(f"{match_list[0][0]['Lisans Numarası']:>3}", end='  ')
        print(f"{match_list[0][0]['Puan']['puan']:>3}", end='  ')
        print(f"{'BYE':>8}")
        match_list[0][0]['Puan']['puan'] += 1
    # maç sayısı çift iken bye olmadığı için ek bir düzenleme yapılmadan yazdırılır
    else:
        for table in range(len(match_list)):
            print(f"{table + 1:>3}", end='  ')
            print(f"{match_list[table][0]['BSNo']:>4}", end='  ')
            print(f"{match_list[table][0]['Lisans Numarası']:>3}", end=' ')
            print(f"{match_list[table][0]['Puan']['puan']:>4.2f}", end='  ')
            print(f"{match_list[table][1]['Puan']['puan']:>8.2f}", end='  ')
            print(f"{match_list[table][1]['Lisans Numarası']:>3}", end='  ')
            print(f"{match_list[table][1]['BSNo']:>4}")


# eşleştirme tablosunu yazdıran fonksiyon
def print_pair_table(match_list, general_data_list):
    print(f"{'Beyazlar':>14}", end=' ')
    print(f"{'Siyahlar':>22}")
    print(f"{'MNo':>3}", end='  ')
    print(f"{'BSNo':>4}", end='  ')
    print(f"{'LNo':>3}", end='  ')
    print(f"{'Puan':>4}", end='  ')
    print(f"{'-':}", end='  ')
    print(f"{'Puan':>4}", end='  ')
    print(f"{'LNo':>3}", end='  ')
    print(f"{'BSNo':>4}")
    print(f"{'---'}", end='  ')
    print(f"{'----'}", end='  ')
    print(f"{'---'}", end='  ')
    print(f"{'----'}", end='  ')
    print(f"{'   ----'}", end='  ')
    print(f"{'---'}", end='  ')
    print(f"{'----'}")
    make_pair_table(match_list, general_data_list)


# maç sonucunu sınırlamalarına göre kullanıcıdan alan fonksiyon
def get_match_result(match, round_number, match_list):
    # iste;nilen baçın indexine bakılıp kullanıcıdan o maçın sonucunu girilmesi istenir
    while True:
        try:
            match_result = int(input(str(round_number + 1) + '.Turda ' + str(
                match_list.index(match)) + '. masada oynanan maçın sonucunu giriniz(0-5):'))
            # eğer maç sonucu istenilen şekilde girilmediyse tekrar sorulur
            while match_result not in [0, 1, 2, 3, 4, 5]:
                print(HATA)
                match_result = int(input(str(round_number + 1) + '.Turda ' + str(
                    match_list.index(match)) + '. masada oynanan maçın sonucunu giriniz(0-5):'))
            break
        except ValueError:
            print(HATA2)
    # maç sonucu döndürülür
    return match_result


# maç sonuçlarına göre puanları güncelleyen ve gerekli verileri ekleyen fonksiyon
def update_points(match_list, round_number, number_of_rounds, general_data_list):
    # maç listesinde ilk eleman bye olduğu için ilk eleman dışında maç listesinde dönen bir for döngüsü oluşturulur
    if len(general_data_list) % 2 != 0:
        # maç listesi tek sayıysa bye geçen olduğu için index 1'den bailayarak döngü oluşturulur
        for match in match_list[1:]:
            # maç sonucu kullanıcıdan alınır
            match_result = get_match_result(match, round_number, match_list)
            # maç sonucuna göre kullanıcının puanı arttılır
            if match_result == 0:
                match[0]['Puan']['puan'] += HALF_POINT
                match[1]['Puan']['puan'] += HALF_POINT
                match[0]['Maç Sonuçları'].append(['½', match[0]['Renk']])
                match[1]['Maç Sonuçları'].append(['½', match[1]['Renk']])
                # eşleşme bozma fonksiyonunda kullanılmak için rakip puanları eklenir
                match[0]['Rakip Puanları'].append(match[1]['Puan'])
                match[1]['Rakip Puanları'].append(match[0]['Puan'])
            elif match_result == 1:
                match[0]['Puan']['puan'] += HIGHEST_POINT
                match[0]['Maç Sonuçları'].append(['1', match[0]['Renk']])
                match[1]['Maç Sonuçları'].append(['0', match[1]['Renk']])
                match[0]['Rakip Puanları'].append(match[1]['Puan'])
                match[1]['Rakip Puanları'].append(match[0]['Puan'])
            elif match_result == 2:
                match[1]['Puan']['puan'] += HIGHEST_POINT
                match[0]['Maç Sonuçları'].append(['0', match[0]['Renk']])
                match[1]['Maç Sonuçları'].append(['1', match[1]['Renk']])
                match[0]['Rakip Puanları'].append(match[1]['Puan'])
                match[1]['Rakip Puanları'].append(match[0]['Puan'])
            elif match_result == 3:
                # eşleştirme bozma fonksiyonlarında kullanılmak için hayali rakip puanları eklenir
                match[0]['Rakip Puanları'].append(
                    {'puan': match[0]['Puan']['puan'] + ((number_of_rounds - (round_number + 1)) * 0.5)})
                match[1]['Rakip Puanları'].append(
                    {'puan': match[1]['Puan']['puan'] + ((number_of_rounds - (round_number + 1)) * 0.5)})
                match[0]['Puan']['puan'] += HIGHEST_POINT
                match[0]['Maç Sonuçları'].append(['+', match[0]['Renk']])
                match[1]['Maç Sonuçları'].append(['-', match[1]['Renk']])

            elif match_result == 4:
                # eşleştirme bozma fonksiyonlarında kullanılmak için hayali rakip puanları eklenir
                match[0]['Rakip Puanları'].append(
                    {'puan': match[0]['Puan']['puan'] + ((number_of_rounds - (round_number + 1)) * 0.5)})
                match[1]['Rakip Puanları'].append(
                    {'puan': match[1]['Puan']['puan'] + ((number_of_rounds - (round_number + 1)) * 0.5)})
                match[1]['Puan']['puan'] += HIGHEST_POINT
                match[1]['Maç Sonuçları'].append(['+', match[1]['Renk']])
                match[0]['Maç Sonuçları'].append(['-', match[0]['Renk']])
            else:
                match[1]['Maç Sonuçları'].append(['-', match[1]['Renk']])
                match[0]['Maç Sonuçları'].append(['-', match[0]['Renk']])
                match[0]['Rakip Puanları'].append(
                    {'puan': match[0]['Puan']['puan'] + ((number_of_rounds - (round_number + 1)) * 0.5)})
                match[1]['Rakip Puanları'].append(
                    {'puan': match[1]['Puan']['puan'] + ((number_of_rounds - (round_number + 1)) * 0.5)})
    else:
        # çift sayı ise normal döngü oluşturulur
        for match in match_list:
            # maç sonucu kullanıcıdan alınır
            match_result = get_match_result(match, round_number, match_list)
            # maç sonucuna göre kullanıcının puanı arttılır
            if match_result == 0:
                match[0]['Puan']['puan'] += HALF_POINT
                match[1]['Puan']['puan'] += HALF_POINT
                match[0]['Maç Sonuçları'].append(['½', match[0]['Renk']])
                match[1]['Maç Sonuçları'].append(['½', match[1]['Renk']])
                # eşleşme bozma fonksiyonunda kullanılmak için rakip puanları eklenir
                match[0]['Rakip Puanları'].append(match[1]['Puan'])
                match[1]['Rakip Puanları'].append(match[0]['Puan'])
            elif match_result == 1:
                match[0]['Puan']['puan'] += HIGHEST_POINT
                match[0]['Maç Sonuçları'].append(['1', match[0]['Renk']])
                match[1]['Maç Sonuçları'].append(['0', match[1]['Renk']])
                match[0]['Rakip Puanları'].append(match[1]['Puan'])
                match[1]['Rakip Puanları'].append(match[0]['Puan'])
            elif match_result == 2:
                match[1]['Puan']['puan'] += HIGHEST_POINT
                match[0]['Maç Sonuçları'].append(['0', match[0]['Renk']])
                match[1]['Maç Sonuçları'].append(['1', match[1]['Renk']])
                match[0]['Rakip Puanları'].append(match[1]['Puan'])
                match[1]['Rakip Puanları'].append(match[0]['Puan'])
            elif match_result == 3:
                # eşleştirme bozma fonksiyonlarında kullanılmak için hayali rakip puanları eklenir
                match[0]['Rakip Puanları'].append(
                    {'puan': match[0]['Puan']['puan'] + ((number_of_rounds - (round_number + 1)) * 0.5)})
                match[1]['Rakip Puanları'].append(
                    {'puan': match[1]['Puan']['puan'] + ((number_of_rounds - (round_number + 1)) * 0.5)})
                match[0]['Puan']['puan'] += HIGHEST_POINT
                match[0]['Maç Sonuçları'].append(['+', match[0]['Renk']])
                match[1]['Maç Sonuçları'].append(['-', match[1]['Renk']])
            elif match_result == 4:
                # eşleştirme bozma fonksiyonlarında kullanılmak için hayali rakip puanları eklenir
                match[0]['Rakip Puanları'].append(
                    {'puan': match[0]['Puan']['puan'] + ((number_of_rounds - (round_number + 1)) * 0.5)})
                match[1]['Rakip Puanları'].append(
                    {'puan': match[1]['Puan']['puan'] + ((number_of_rounds - (round_number + 1)) * 0.5)})
                match[1]['Puan']['puan'] += HIGHEST_POINT
                match[1]['Maç Sonuçları'].append(['+', match[1]['Renk']])
                match[0]['Maç Sonuçları'].append(['-', match[0]['Renk']])

            else:
                match[1]['Maç Sonuçları'].append(['-', match[1]['Renk']])
                match[0]['Maç Sonuçları'].append(['-', match[0]['Renk']])
                match[0]['Rakip Puanları'].append(
                    {'puan': match[0]['Puan']['puan'] + ((number_of_rounds - (round_number + 1)) * 0.5)})
                match[1]['Rakip Puanları'].append(
                    {'puan': match[1]['Puan']['puan'] + ((number_of_rounds - (round_number + 1)) * 0.5)})


def main():
    # oyuncu verilerini koymak için bir liste oluşturulur
    general_data_list = []
    # lisans numarası alınır
    while True:
        try:
            # lisans numarası alınır
            license_number = int(input('Oyuncunun lisans numarasını giriniz - programdan çıkmak için '
                                       '0 ya da negatif girebilirsiniz- : '))
            while license_number <= 0:
                exit('Program Sonlandırılmıştır.')
            break
        except ValueError:
            print(HATA2)
    # lisans numarası 0 ya da 0'dan düşük girilirse programdan çıkılır
    while license_number > 0:
        # boş bir dictionary oluşturulur
        data_dict = {}
        # her bir oyuncunun verileri ayrı bir dictionary'de tutulur
        # kullanıcıdan isim alınır ve türkçe harflere göre büyütülür
        name = input('Oyuncunun adını-soyadını giriniz: ').replace('i', 'İ').replace('ı', 'I').upper()
        # kullanıcıdan elo istenilen aralıkta alınır
        elo = get_number('Oyuncunun ELO’sunu giriniz -en az 1000, yoksa 0- :')
        # kullanıcdan ukd istenilen aralıkta alınır
        ukd = get_number('Oyuncunun UKD’sini giriniz -en az 1000, yoksa 0- :')
        # her veri dictionarye atanır
        data_dict['Ad-Soyad'] = name
        data_dict['ELO'] = elo
        data_dict['UKD'] = ukd
        data_dict['Lisans Numarası'] = license_number
        # puan dictionary olarak konur ki güncellendiğinde eklendiği her tarafa güncellensin
        data_dict['Puan'] = {'puan': 0}
        data_dict['Rakipler'] = []
        data_dict['O2R'] = [' ', ' ']
        data_dict['Rakip Puanları'] = []
        data_dict['Maç Sonuçları'] = []
        data_dict['BH1'] = 0
        data_dict['BH2'] = 0
        data_dict['SB'] = 0
        data_dict['GS'] = 0
        data_dict['b'] = 0
        data_dict['s'] = 0
        # oluşturulan dictionary listeye eklenir
        general_data_list.append(data_dict)
        # lisans numarası alınır ve eşsiz olup olmadığına bakılır
        license_number = unique_number(general_data_list)
    # veri listesi dökümanda istenilen önceliğe göre sıralanır
    sort(general_data_list)
    # başlangıç sıralaması yazdırılır
    print_starting_table(general_data_list)
    # tur sayısı alınır
    number_of_rounds = get_number_of_rounds(len(general_data_list))
    # ilk renk alınır ve oyunculara renkler dağıtılır
    get_and_give_colours(general_data_list)
    # tur sayısı kadar for döngüsüne girilir
    for round_number in range(number_of_rounds):
        # yapılan maçları tutmak için her tur sıfırlanacak bir liste oluşturulur
        match_list = []
        # 1. turdayken ilk tur için yapılan eşleştirme fonksiyonu çağırılır
        if round_number + 1 == 1:
            first_pairing(general_data_list, match_list, number_of_rounds)
        # 1.  tur dışındaki turlar için diğer eşleştirme fonksiyonu çağırılır
        else:
            other_pairings(general_data_list, match_list, number_of_rounds, round_number)
        # eşleştirme tablosu yazdırılır
        print(str(round_number + 1) + '. Tur Eşleştirme Listesi')
        print_pair_table(match_list, general_data_list)
        # maç sonuçlarına göre puanlar güncellenir
        update_points(match_list, round_number, number_of_rounds, general_data_list)
        # döngü sonunda veri listesi istenilen önceliğe göre tekrar sıralanır
        sort(general_data_list)
    # Oyuncuların bh puanları hesaplanır
    calculate_bh(general_data_list)
    # Oyuncuların sb puanları hesaplanır
    calculate_sb(general_data_list)
    # Oyuncuların gs puanları hesaplanır
    calculate_gs(general_data_list)
    # eklenen eşleştirme bozma puanlarıyla veri listesi tekrar sıralanır
    sort(general_data_list)
    # nihai sıralama yazdırılır
    ultimate_ranking(general_data_list)
    # çapraz tablo yazdırılır
    cross_table(general_data_list, number_of_rounds)


main()
