import sys
import csv
import math

# 上位から取得したいランクの数
WANT_TOP_RANK = 10


# csvファイルからリスト型に変換したデータに変換する
def conversionCsv(file):
	csv_file = open(file, "r", errors="", newline="")
	f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

	# header: create_timestamp,player_id,score
	next(f)
	
	conversionData = []
	for row in f:
		row[2] = int(row[2])
		conversionData.append(row)
	return conversionData


# プレイヤーと平均スコアの辞書型配列を返す
def get_player_average_score_dict(play_log_list):
	# プレイヤーに対するスコアの合計とプレイ数を管理する辞書型配列を作成
	player_data_dict = {}
	for play_log_item in play_log_list:
		player = play_log_item[1]
		score = play_log_item[2]
		if player in player_data_dict:
			player_data_dict[player]["score"] += score
			player_data_dict[player]["num_of_play"] += 1
		else:
			player_data_dict[player] = {"score": score, "num_of_play": 1}

	# 平均スコアを算出するための計算
	player_average_score_data = {}
	for player in player_data_dict:
		player_average_score_data[player] = player_data_dict[player]["score"] / player_data_dict[player]["num_of_play"]
	return player_average_score_data


def get_top_rank(rank, player_average_score_dict):
	# ソートした際に型が変わるので元に戻す
	sorted_player_average_score_dict = {}
	for sorted_data in sorted(player_average_score_dict.items(), key=lambda player: player[1], reverse=True):
		sorted_player_average_score_dict[sorted_data[0]] = sorted_data[1]

	# 上位のランキングを作成
	rank_sum = 0
	rank_index = 1
	score_index = round(sorted_player_average_score_dict[next(iter(sorted_player_average_score_dict))])
	ranking_dict = {rank_index: {}}
	for player in sorted_player_average_score_dict:
		rank_sum += 1
		if score_index == round(sorted_player_average_score_dict[player]):
			ranking_dict[rank_index][player] = round(sorted_player_average_score_dict[player])
		else:
			if rank_sum > rank:
				break
			rank_index += len(ranking_dict[rank_index])
			score_index = round(sorted_player_average_score_dict[player])
			ranking_dict[rank_index] = {}
			ranking_dict[rank_index][player] = round(sorted_player_average_score_dict[player])

	return ranking_dict


def print_rank(ranking):
	for rank in ranking:
		for player_data in sorted(ranking[rank].items(), key=lambda x:x[0]):
			content = [str(rank), player_data[0], str(player_data[1])]
			print(",".join(content))


def main():
	file = sys.argv[1]
	
	play_log_list = conversionCsv(file)
	print("rank,player_id,mean_score")

	if len(play_log_list) > 0 :
		player_average_score_dict = get_player_average_score_dict(play_log_list)
		# print(player_average_score_dict['player372'])
		top_rank = get_top_rank(WANT_TOP_RANK, player_average_score_dict)
		print_rank(top_rank)


if __name__ == "__main__":
	main()