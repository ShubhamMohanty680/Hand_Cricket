# import cv2
# import multiprocessing
# import numpy as np
# import mediapipe as mp
# import pickle
# import warnings

# warnings.filterwarnings("ignore")

# with open('hand_model.pkl', 'rb') as f:
#     rf = pickle.load(f)

# hands = mp.solutions.hands
# mp_styles = mp.solutions.drawing_styles

# word_to_num = {
#     'zero': 0, 'one': 1, 'two': 2, 'three': 3,
#     'four': 4, 'six': 6
# }

# def camera(index, wind_name, queue, stop_event, shared_predictions):
#     fm_model = hands.Hands(static_image_mode=True,
#                            min_detection_confidence=0.9,
#                            min_tracking_confidence=0.9,
#                            max_num_hands=4)

#     vid = cv2.VideoCapture(index)
#     predictions = []
#     waiting_for_next = False

#     while True:
#         if stop_event.is_set():
#             break

#         b, f = vid.read()
#         if not b:
#             break

#         rgb = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
#         result = fm_model.process(rgb)

#         pred = None

#         if result.multi_hand_landmarks:
#             mp.solutions.drawing_utils.draw_landmarks(
#                 image=f,
#                 landmark_list=result.multi_hand_landmarks[0],
#                 connections=hands.HAND_CONNECTIONS,
#                 landmark_drawing_spec=mp_styles.get_default_hand_landmarks_style(),
#                 connection_drawing_spec=mp_styles.get_default_hand_connections_style()
#             )

#             hand = []
#             for i in result.multi_hand_landmarks[0].landmark:
#                 hand.extend([i.x, i.y, i.z])

#             if hand:
#                 pred = rf.predict([hand])[0]

#                 if pred == 'closed':
#                     waiting_for_next = True
#                     cv2.putText(f, "Ready for next gesture", (30, 120),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

#                 elif waiting_for_next and pred != 'closed':
#                     predictions.append(pred)
#                     waiting_for_next = False
#                     print(f"{wind_name} Gesture stored: {pred}")
#                     shared_predictions.put((wind_name, pred))

#         display_text = pred if pred is not None else "No Hand"
#         cv2.putText(f, f"{display_text} ({len(predictions)}/6)", (30, 70),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#         if stop_event.is_set():
#             cv2.putText(f, "OUT!", (200, 200),
#                         cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

#         cv2.imshow(wind_name, f)

#         if len(predictions) >= 6:
#             break

#         if cv2.waitKey(1) & 255 == ord('q'):
#             break

#     vid.release()
#     cv2.destroyWindow(wind_name)
#     queue.put(predictions)

# def play_inning(batter_name, bowler_name, batter_cam, bowler_cam):
#     q1 = multiprocessing.Queue()
#     q2 = multiprocessing.Queue()
#     shared_predictions = multiprocessing.Queue()
#     stop_event = multiprocessing.Event()

#     p1 = multiprocessing.Process(target=camera, args=(batter_cam, 'Batter', q1, stop_event, shared_predictions))
#     p2 = multiprocessing.Process(target=camera, args=(bowler_cam, 'Bowler', q2, stop_event, shared_predictions))

#     p1.start()
#     p2.start()

#     batter_seq = []
#     bowler_seq = []

#     while not stop_event.is_set():
#         if not shared_predictions.empty():
#             cam_name, word = shared_predictions.get()
#             num = word_to_num.get(word, -1)

#             if cam_name == 'Batter':
#                 batter_seq.append(num)
#             elif cam_name == 'Bowler':
#                 bowler_seq.append(num)

#             for i in range(min(len(batter_seq), len(bowler_seq))):
#                 if batter_seq[i] == bowler_seq[i] and batter_seq[i] != -1:
#                     print("Out detected at position", i + 1)
#                     stop_event.set()
#                     break

#         if len(batter_seq) >= 6 and len(bowler_seq) >= 6:
#             break

#     p1.join()
#     p2.join()

#     result1 = q1.get()
#     result2 = q2.get()

#     batter_nums = [word_to_num.get(w, -1) for w in result1]
#     bowler_nums = [word_to_num.get(w, -1) for w in result2]

#     runs = 0
#     for i, (b, bowl) in enumerate(zip(batter_nums, bowler_nums)):
#         if b == bowl:
#             break
#         if b != -1:
#             runs += b

#     print(f"{batter_name} scored {runs} runs.")
#     return runs

# if __name__ == '__main__':
#     player1_name = input("Enter name for Player 1 (Camera 1): ")
#     player2_name = input("Enter name for Player 2 (Camera 2): ")

#     # Toss
#     toss_call = input(f"{player1_name}, choose Head or Tail: ").strip().lower()
#     toss_result = np.random.choice(['head', 'tail'])

#     print(f"Toss result: {toss_result.upper()}")
#     if toss_call == toss_result:
#         toss_winner = player1_name
#         toss_loser = player2_name
#         # winner_cam = 1
#         # loser_cam = 2
#     else:
#         toss_winner = player2_name
#         toss_loser = player1_name
#         # winner_cam = 2
#         # loser_cam = 1

#     # Let toss winner decide
#     while True:
#         choice = input(f"{toss_winner}, do you choose to 'bat' or 'bowl' first? ").strip().lower()
#         if choice in ['bat', 'bowl']:
#             break
#         print("Invalid choice. Please enter 'bat' or 'bowl'.")

#     print(f"\n{toss_winner} won the toss and chose to {choice.upper()} first.")

#     if choice == 'bat':
#         first_batter, first_bowler = toss_winner, toss_loser
#         first_batter_cam, first_bowler_cam = winner_cam, loser_cam
#     else:
#         first_batter, first_bowler = toss_loser, toss_winner
#         first_batter_cam, first_bowler_cam = loser_cam, winner_cam

#     print(f"\n{first_batter} will bat first using Camera {first_batter_cam}.")
#     print(f"{first_bowler} will bowl first using Camera {first_bowler_cam}.")

#     print("\n--- FIRST INNING ---")
#     first_inning_score = play_inning(first_batter, first_bowler, first_batter_cam, first_bowler_cam)

#     print("\n--- SECOND INNING ---")
#     second_inning_score = play_inning(first_bowler, first_batter, first_bowler_cam, first_batter_cam)

#     print("\n--- FINAL RESULT ---")
#     print(f"{first_batter}: {first_inning_score} runs")
#     print(f"{first_bowler}: {second_inning_score} runs")

#     if first_inning_score > second_inning_score:
#         print(f"{first_batter} wins by {first_inning_score - second_inning_score} runs!")
#     elif second_inning_score > first_inning_score:
#         print(f"{first_bowler} wins by {6 - len(str(second_inning_score))} wickets!")
#     else:
#         print("Match Tied!")




import cv2
import multiprocessing
import numpy as np
import mediapipe as mp
import pickle
import warnings
import time

warnings.filterwarnings("ignore")

# Load trained model
with open('hand_model.pkl', 'rb') as f:
    rf = pickle.load(f)

# MediaPipe setup
hands = mp.solutions.hands
mp_styles = mp.solutions.drawing_styles

# Mapping gestures to runs
word_to_num = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3,
    'four': 4, 'six': 6
}

def camera(index, wind_name, queue, stop_event, shared_predictions):
    fm_model = hands.Hands(static_image_mode=True,
                           min_detection_confidence=0.9,
                           min_tracking_confidence=0.9,
                           max_num_hands=4)

    vid = cv2.VideoCapture(index)
    predictions = []
    waiting_for_next = False

    while True:
        if stop_event.is_set():
            break

        b, f = vid.read()
        if not b:
            break

        rgb = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
        result = fm_model.process(rgb)
        pred = None

        if result.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                image=f,
                landmark_list=result.multi_hand_landmarks[0],
                connections=hands.HAND_CONNECTIONS,
                landmark_drawing_spec=mp_styles.get_default_hand_landmarks_style(),
                connection_drawing_spec=mp_styles.get_default_hand_connections_style()
            )

            hand = []
            for i in result.multi_hand_landmarks[0].landmark:
                hand.extend([i.x, i.y, i.z])

            if hand:
                pred = rf.predict([hand])[0]

                if pred == 'closed':
                    waiting_for_next = True
                    cv2.putText(f, "Ready for next gesture", (30, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
                elif waiting_for_next and pred != 'closed':
                    predictions.append(pred)
                    waiting_for_next = False
                    print(f"{wind_name} Gesture stored: {pred}")
                    shared_predictions.put((wind_name, pred))

        display_text = pred if pred is not None else "No Hand"
        cv2.putText(f, f"{display_text} ({len(predictions)}/6)", (30, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if stop_event.is_set():
            cv2.putText(f, "OUT!", (200, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

        cv2.imshow(wind_name, f)

        if len(predictions) >= 6:
            break

        if cv2.waitKey(1) & 255 == ord('q'):
            break

    vid.release()
    cv2.destroyWindow(wind_name)
    queue.put(predictions)

def play_inning(batter_name, bowler_name, batter_cam, bowler_cam):
    q1 = multiprocessing.Queue()
    q2 = multiprocessing.Queue()
    shared_predictions = multiprocessing.Queue()
    stop_event = multiprocessing.Event()

    p1 = multiprocessing.Process(target=camera, args=(batter_cam, 'Batter', q1, stop_event, shared_predictions))
    p2 = multiprocessing.Process(target=camera, args=(bowler_cam, 'Bowler', q2, stop_event, shared_predictions))

    p1.start()
    p2.start()

    batter_seq = []
    bowler_seq = []

    while not stop_event.is_set():
        if not shared_predictions.empty():
            cam_name, word = shared_predictions.get()
            num = word_to_num.get(word, -1)

            if cam_name == 'Batter':
                batter_seq.append(num)
            elif cam_name == 'Bowler':
                bowler_seq.append(num)

            for i in range(min(len(batter_seq), len(bowler_seq))):
                if batter_seq[i] == bowler_seq[i] and batter_seq[i] != -1:
                    print("Out detected at position", i + 1)
                    stop_event.set()
                    break

        if len(batter_seq) >= 6 and len(bowler_seq) >= 6:
            break

    p1.join()
    p2.join()

    result1 = q1.get()
    result2 = q2.get()

    batter_nums = [word_to_num.get(w, -1) for w in result1]
    bowler_nums = [word_to_num.get(w, -1) for w in result2]

    runs = 0
    outs = 0
    for i, (b, bowl) in enumerate(zip(batter_nums, bowler_nums)):
        if b == bowl:
            outs += 1
            break
        if b != -1:
            runs += b

    return runs, outs

if __name__ == '__main__':
    player1_name = input("Enter name for Player 1 (Camera 1): ")
    player2_name = input("Enter name for Player 2 (Camera 2): ")
    
    # Toss chosen by player 1
    toss_call = input(f"{player1_name}, choose Head or Tail: ").strip().lower() 
    toss_result = np.random.choice(['head', 'tail'])
    print(f"Toss result: {toss_result.upper()}")

    if toss_call == toss_result:
        toss_winner = player1_name
        toss_loser = player2_name
        winner_cam = 0
        loser_cam = 1
    else:
        toss_winner = player2_name
        toss_loser = player1_name
        winner_cam = 1
        loser_cam = 0

    while True:
        choice = input(f"{toss_winner}, do you choose to 'bat' or 'bowl' first? ").strip().lower()
        if choice in ['bat', 'bowl']:
            break
        print("Invalid choice. Please enter 'bat' or 'bowl'.")

    print(f"\n{toss_winner} won the toss and chose to {choice.upper()} first.")

    if choice == 'bat':
        first_batter, first_bowler = toss_winner, toss_loser
        first_batter_cam, first_bowler_cam = winner_cam, loser_cam
    else:
        first_batter, first_bowler = toss_loser, toss_winner
        first_batter_cam, first_bowler_cam = loser_cam, winner_cam

    print(f"\n{first_batter} will bat first using Camera {first_batter_cam}.")
    print(f"{first_bowler} will bowl first using Camera {first_bowler_cam}.")

    print("\n--- FIRST INNING ---")
    first_inning_score, _ = play_inning(first_batter, first_bowler, first_batter_cam, first_bowler_cam)

    print("\n--- SECOND INNING ---")
    second_inning_score, second_inning_outs = play_inning(first_bowler, first_batter, first_bowler_cam, first_batter_cam)

    print("\n--- FINAL RESULT ---")
    print(f"{first_batter}: {first_inning_score} runs")
    print(f"{first_bowler}: {second_inning_score} runs")

    if first_inning_score > second_inning_score:
        print(f"{first_batter} wins by {first_inning_score - second_inning_score} runs!")
    elif second_inning_score > first_inning_score:
        wickets_remaining = 6 - second_inning_outs
        print(f"{first_bowler} wins by {wickets_remaining} wicket(s)!")
    else:
        print("Match Tied!")

