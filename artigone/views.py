from django.shortcuts import render
from artigone.models import *
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect,HttpResponse
import random
import json
from ast import literal_eval

def delete_question_answer_after_game(inactive_game):
    inactive_questions = Question.objects.filter(game = inactive_game)
    for que in inactive_questions:
        inactive_options = Option.objects.filter(question=que)
        for opt in inactive_options:
            opt.delete()
        que.delete()

def initiateGameView(request):
    if request.user.is_authenticated:
        current_player_playing_game = Game.objects.filter(Q(player1=request.user)|Q(player2=request.user), Q(status='paired')|Q(status='playing')|Q(status='submitted'))
        if current_player_playing_game:
            current_player_playing_game = current_player_playing_game[0]
            current_player_playing_game.status = 'inactive'
            current_player_playing_game.save()
            Game.objects.filter(Q(player1=request.user) | Q(player2=request.user)).update(status='inactive')
            delete_question_answer_after_game(current_player_playing_game)

        active_game = Game.objects.filter(status='on_hold').exclude(player1=request.user)
        current_player_game = Game.objects.filter(Q(status='active')|Q(status='on_hold'), player1=request.user)
        if current_player_game:
            current_player_game = current_player_game[0]
            if current_player_game.status == 'on_hold':
                data = {
                    'status' : 'wait'
                }
                return JsonResponse(data)
            else:
                current_player_game.status = 'paired'
                current_player_game.save()
                data = {
                    'player1' : current_player_game.player1.username,
                    'player2' : current_player_game.player2.username,
                }
                return JsonResponse(data)

        if not active_game:
            new_game = Game(player1=request.user, score=0, status='on_hold')
            new_game.save()
            data = {
                'status' : 'wait'
            }
            return JsonResponse(data)
        else:
            active_game=active_game[0]
            active_game.player2 = request.user
            active_game.status = 'active'
            active_game.save()
            data = {
                'player1' : active_game.player1.username,
                'player2' : active_game.player2.username,
            }
            return JsonResponse(data)
    else:
        return HttpResponse('Nice try but...Access Denied', content_type="text/plain")

def displayGameView(request):
    if request.user.is_authenticated:
        game_paired = Game.objects.filter(Q(player1=request.user)|Q(player2=request.user), status='paired')
        game_playing = Game.objects.filter(Q(player1=request.user)|Q(player2=request.user), Q(status='submitted')|Q(status='playing') )
        if game_paired:
            game_paired = game_paired[0]
            all_question_images = list(PrimaryImage.objects.all())
            all_option_images = list(SecondaryImage.objects.all())
            random.shuffle(all_question_images)
            random.shuffle(all_option_images)
            game_paired.status = 'playing'
            game_paired.save()
            data = {}
            data["game"]={}
            data["game"]["id"] = game_paired.pk
            data["game"]["question"] = []
            count_option = 0
            for i in range(5):
                new_question = Question(game=game_paired, image=all_question_images[i])
                question_image = all_question_images[i]
                new_question.save()
                question_data = {}
                question_data["id"] = new_question.pk
                question_data["url"] = question_image.primary_image_url
                question_data["option"] = []
                for j in range(4):
                    new_option = Option(question=new_question, image=all_option_images[count_option])
                    option_image = all_option_images[count_option]
                    new_option.save()
                    count_option += 1
                    option_data = {}
                    option_data["id"] = new_option.pk
                    option_data["url"] = option_image.secondary_image_url
                    question_data["option"].append(option_data)
                data["game"]["question"].append(question_data)

        elif game_playing:
            game_playing = game_playing[0]
            data = {}
            data["game"]={}
            data["game"]["id"] = game_playing.pk
            data["game"]["question"] = []
            game_questions = Question.objects.filter(game = game_playing)
            for i in game_questions:
                question_data = {}
                question_data["id"] = i.pk
                question_data["url"] = i.image.primary_image_url
                question_data["option"] = []
                game_question_options = Option.objects.filter(question = i)
                for j in game_question_options:
                    option_data = {}
                    option_data["id"] = j.pk
                    option_data["url"] = j.image.secondary_image_url
                    question_data["option"].append(option_data)
                data["game"]["question"].append(question_data)


        else:
            data={}
            data = {
                "message": "Uh oh, seems like your opponent left the Game."
            }

    ### Handle the inactive situation
        return JsonResponse(data, safe=False)

    else:
        return HttpResponse('Nice try but...Access Denied', content_type="text/plain")


def submitGameView(request):
    if request.user.is_authenticated:
        solution_dict = {}
        solution_dict = dict(request.POST.lists())
        game_id = solution_dict['game_id'][0]
        solution_dict = solution_dict['solution'][0]
        game_submitted = Game.objects.get(pk=game_id)

        if game_submitted.status == 'playing':
            game_submitted.first_solution = solution_dict
            game_submitted.status = 'submitted'
            game_submitted.save()
            data = {
                'status' : 'wait'
            }
            return JsonResponse(data)

        elif game_submitted.status == 'submitted':
            first_solution = game_submitted.first_solution
            second_solution = solution_dict
            first_solution = literal_eval(first_solution)
            second_solution = literal_eval(second_solution)
            score=0
            for i in first_solution:
                if first_solution[i] == second_solution[i]:
                    score += 1
            game_submitted.score = score
            game_submitted.status = 'finished'
            delete_question_answer_after_game(game_submitted)
            game_submitted.save()
            message = "Your score is " + str(score)+"!!"
            data = {
                'message' : message
            }
            return JsonResponse(data)

        else:
            data = {
                "message": "Uh oh, seems like your opponent left the Game."
            }
            return JsonResponse(data)

        print(solution_dict)
    else:
        return HttpResponse('Nice try but...Access Denied', content_type="text/plain")

def waitForScoreView(request):
    if request.user.is_authenticated:
        solution_dict = dict(request.POST.lists())
        game_id = solution_dict['game_id'][0]
        solution_dict = solution_dict['solution'][0]
        game_submitted = Game.objects.get(pk=game_id)

        if game_submitted.status == 'submitted':
            data = {
                'status' : 'wait'
            }
            return JsonResponse(data)

        elif game_submitted.status == 'finished':
            score = game_submitted.score
            message = "Your score is " + str(score) + "!!"
            data = {
                'message' : message
            }
            return JsonResponse(data)
        else:
            data = {
                "message": "Uh oh, seems like your opponent left the Game."
            }
            return JsonResponse(data)
    else:
        return HttpResponse('Nice try but...Access Denied', content_type="text/plain")
