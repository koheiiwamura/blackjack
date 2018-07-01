import random


deck = [number for number in range(1, 14) for face_card in ["heart", "club", "clover", "diamond"]]
line = "-------------------------------------"


def reward_of_result(player_points, dealer_points, bets):
    if dealer_points > 21:
        reward = bets * 2
        print("ディーラーがBurnoutしているので、あなたの勝ちです\n賭け金の2倍のお金(%s円)が手に入りました" % reward)
    else:
        if player_points == dealer_points:
            print("引き分けです。賭け金(%s)のみ返金されました" % bets)
            reward = bets
        elif player_points > dealer_points:
            reward = bets * 2
            print("あなたの勝ちです。賭け金の2倍のお金(%s円)が手に入りました" % reward)
        else:
            print("あなたの負けです。賭け金(%s円)を失いました。" % bets)
            reward = 0
    return reward


def card_to_point(card):
    if card <= 10 and card != 1:
        return card
    else:
        return 10


def change_point_for_ace(hand, points):
    if points >=21:
        for ace in range(hand.count(1)):
            points -= 9
            if points <=21:
                break
    return points


def from_point_to_face_card(point):
    face_card_dict = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}
    return face_card_dict[point] if point in face_card_dict else point


def show_hands_list(hands):
    hands_list = []
    for card in hands:
        hands_list.append(from_point_to_face_card(card))
    return hands_list


def dealers_turn(dealer_hands):
    dealer_points = 0
    for card in dealer_hands:
        dealer_points += card_to_point(card)
    while 1:
        if dealer_points < 17 or (dealer_points == 17 and 1 in dealer_hands):
            if dealer_points == 17 and 1 in dealer_hands:
                print("ディーラーのHandは17ですが、Aがあるため1枚引きます")
            draw_card = random.choice(deck)
            point = card_to_point(draw_card)
            dealer_points += point
            print("ディーラーは %s を引きました" % from_point_to_face_card(draw_card))
        else:
            print("ディーラーの手札が決まりました。合計 %s です" % dealer_points)
            return dealer_points
            break


def play_blackjack(pocket_money):
    player_points = 0
    player_hands = []
    face_card = [1, 11, 12, 13]

    while 1:
        try:
            bets = int(input("掛け金を入力してください(所持金： %s円)" % pocket_money))
            if bets > pocket_money:
                print("そんなにお金はありません")
            else:
                break
        except Exception:
            print("正しく入力してください")

    print("\n\nお互い2枚ずつ配ります\n")
    player_hands = random.sample(deck, 2)
    dealer_hands = random.sample(deck, 2)

    if dealer_hands[0] in face_card and dealer_hands[1] in face_card:
        print("相手がどちらも絵柄のため、あなたの負けです")
        reward = 0 - bets
        return reward
    if player_hands[0] in face_card and player_hands[1] in face_card:
        print("どちらも絵柄のため、あなたの勝ちです")
        reward = bets * 1.5
        return int(reward)

    player_points = card_to_point(player_hands[0]) + card_to_point(player_hands[1])
    print("ディーラーに配られた最初のカードの1枚：%s" % from_point_to_face_card(dealer_hands[0]))
    print("自分に配られたカード：%s" % show_hands_list(player_hands))
    print("合計ポイント：%s" % player_points)

    while 1:
        cheese = input("\n\nカードを引きますか？0:引く, 1:引かない")
        try:
            cheese = int(cheese)
        except Exception:
            print("正しく入力してください")
            cheese == 1
        if cheese == 0:
            draw_card = random.choice(deck)
            player_hands.append(draw_card)
            point = card_to_point(draw_card)
            player_points += point
            print("%s\nあなたが引いたカード： %s" % (line, from_point_to_face_card(draw_card)))
            print(show_hands_list(player_hands))
            revised_point = change_point_for_ace(player_hands, player_points)
            if player_points > 21 and 1 in player_hands:
                print("合計21以下になるまでAceを1ポイントとして数えます")
            print("\nあなたのカードの合計値：%s\n%s" % (revised_point, line))
            if revised_point > 21:
                print("21を超えてしまいました。あなたの負けです。Burn out")
                reward = 0
                break
        elif cheese == 1:
            print("引かないのでディーラーを待ちます\n%s" % line)
            dealer_points = dealers_turn(dealer_hands)
            player_points = change_point_for_ace(player_hands, player_points)
            reward = reward_of_result(player_points, dealer_points, bets) - bets
            break
        else:
            print("0か1を選んでください")
    return reward


def input_pocket_money():
    while 1:
        try:
            pocket_money = int(input("所持金を入力してください(円)"))
            break
        except Exception:
            print("正しく入力してください")
    return pocket_money


def judge_to_participate(pocket_money):
    while 1:
        if pocket_money <= 0:
            print("見事に破産しました、強制退去です GAMEOVER")
            break
        else:
            if input("ブラックジャックに参加しますか？0:参加する, 他のボタン:参加しない") == "0":
                pocket_money += play_blackjack(pocket_money)
            else:
                print("ゲームを終了します。最終的な所持金は： %s円です" % pocket_money)
                break

if __name__ == "__main__":
    judge_to_participate(input_pocket_money())
