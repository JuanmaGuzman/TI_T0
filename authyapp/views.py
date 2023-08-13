from pickle import LIST
from typing import Dict
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
import json
import random
from datetime import datetime as dt
import time
import datetime
from .models import User, UserToken, AccessTokenRequest, AccessToken

def reset(request):
    if request.method == 'GET':
        print("RESET BD")
        user_db = User.objects.all()
        usertoken_db = UserToken.objects.all()
        accesstoken_db = AccessTokenRequest.objects.all()
        user_db.delete()
        usertoken_db.delete()
        accesstoken_db.delete()
        return HttpResponse("DB's reseted")

@csrf_exempt
def user(request):
    random_string = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ1234567890"
    token_value = ""
    #Mostrar todos los usuarios con link a su info
    if request.method == 'POST':
        usernames_list = []
        user_data = request.body
        dictionary = json.loads(user_data)
        
        if "username" not in dictionary.keys() or "age" not in dictionary.keys() or "name" not in dictionary.keys():
            dicc = {"error": "invalid atributes"}
            json_response = json.dumps(dicc)
            return HttpResponse(json_response, status=400)  

        dic_types = {"username":str,"password":str,"name":str,"age":int,"psu_score":int,"university":str,
        "gpa_score":float,"job":str,"salary":float,"promotion":bool,"hospital":str,"operations":list,
        "medical_debt":float}

        lista_valores = [0,0.0,"not",True]
        for k in dic_types.keys():
            if k not in dictionary.keys():
                for valor in lista_valores:
                    if type(valor) == dic_types[k]:
                        dictionary[k] = valor
                    else:
                        pass

        print(dictionary)
        for k in dictionary.keys():
            if k in dic_types.keys() and type(dictionary[k]) == dic_types[k]:
                pass
            else:
                print(type(dictionary[k]))
                print(dictionary[k])
                print(dic_types[k])
                print("Se cae comparando valores de llaves")
                dicc = {"error": "invalid atributes"}
                json_response = json.dumps(dicc)
                return HttpResponse(json_response, status=400)

        for u in User.objects.all():
            #usernames_list.append(u["username"])
            print(u.username)
            usernames_list.append(u.username)

        else:
            try:
                new_username = dictionary["username"]
                if new_username in usernames_list:
                    dicc = {"error": "user already exists"}
                    json_response = json.dumps(dicc)
                    return HttpResponse(json_response, status=409)

                else:
                    new_user = User(username=dictionary["username"],
                                    password=dictionary["password"],
                                    name=dictionary["name"],
                                    age=dictionary["age"],
                                    psu_score=dictionary["psu_score"],
                                    university=dictionary["university"],
                                    gpa_score=dictionary["gpa_score"],
                                    job=dictionary["job"],
                                    salary=dictionary["salary"],
                                    promotion=dictionary["promotion"],
                                    hospital=dictionary["hospital"],
                                    operations = dictionary["operations"],
                                    medical_debt=dictionary["medical_debt"])
                    new_user.save()
                    user_instance = User.objects.get(username=new_username)
                    for i in range(0,30):
                        pos = random.randint(0,len(random_string) - 1)
                        char = random_string[pos]
                        token_value = token_value + char

                    new_token = UserToken(user=user_instance, token=token_value)
                    new_token.save()
                    dicc = {"id": user_instance.id, "token": token_value}
                    json_response = json.dumps(dicc)
                    return HttpResponse(json_response, status=201)

            except:
                dicc = {"error": "invalid atributes"}
                json_response = json.dumps(dicc)
                return HttpResponse(json_response, status=400)

    else:
        return HttpResponse("GET request")

@csrf_exempt
def user_info(request, user_id):
    #Mostrar info de usuario específico
    dic_types = {"username":str,"password":str,"name":str,"age":int,"psu_score":int,"university":str,
        "gpa_score":float,"job":str,"salary":float,"promotion":bool,"hospital":str,"operations":list,
        "medical_debt":float}

    if request.method == 'DELETE':
        try:
            incoming_token = request.headers["Authorization"]
            incoming_token = UserToken.objects.get(token=incoming_token).token
            real_user_object = UserToken.objects.get(token=incoming_token).user
            real_user_id = real_user_object.id
            incoming_url = request.path
            real_url = "/authyapp/users/" + f"{real_user_id}" 
            if str(real_url) == str(incoming_url):
                real_user_object.delete()
                return HttpResponse("No content", status=204)

            else:
                dicc = {"error": "you do not have access to this resource"}
                json_response = json.dumps(dicc)
                return HttpResponse(json_response, status=403)   
        except:
            dicc = {"error": "invalid token"}
            json_response = json.dumps(dicc)
            return HttpResponse(json_response, status=401)


    elif request.method == 'PATCH':
        usernames_list = []
        user_data = request.body
        dictionary = json.loads(user_data)
        #new_username = dictionary["username"]

        for u in User.objects.all():
            usernames_list.append(u.username)

        try:
            incoming_token = request.headers["Authorization"]
            incoming_token = UserToken.objects.get(token=incoming_token).token
            real_user_object = UserToken.objects.get(token=incoming_token).user
            real_user_id = real_user_object.id
            incoming_url = request.path
            real_url = "/authyapp/users/" + f"{real_user_id}" 
            if str(real_url) == str(incoming_url):
                try:
                    for k in dictionary.keys():
                        if type(dictionary[k]) == dic_types[k]:
                            old_user_data = User.objects.get(id=real_user_id)
                            if "username" in dictionary.keys():
                                old_user_data.username = dictionary["username"]
                                old_user_data.save()
                            if "password" in dictionary.keys():
                                old_user_data.password = dictionary["password"]
                                old_user_data.save()
                            if "name" in dictionary.keys():
                                old_user_data.name = dictionary["name"]
                                old_user_data.save()
                            if "age" in dictionary.keys():
                                old_user_data.age = dictionary["age"]
                                old_user_data.save()
                            if "university" in dictionary.keys():
                                old_user_data.university = dictionary["university"]
                                old_user_data.save()
                            if "gpa_score" in dictionary.keys():
                                old_user_data.gpa_score = dictionary["gpa_score"]
                                old_user_data.save()
                            if "job" in dictionary.keys():
                                old_user_data.job = dictionary["job"]
                                old_user_data.save()
                            if "salary" in dictionary.keys():
                                old_user_data.salary = dictionary["salary"]
                                old_user_data.save()
                            if "promotion" in dictionary.keys():
                                old_user_data.promotion = dictionary["promotion"]
                                old_user_data.save()
                            if "hospital" in dictionary.keys():
                                old_user_data.hospital = dictionary["hospital"]
                                old_user_data.save()
                            if "operations" in dictionary.keys():
                                old_user_data.operations = dictionary["operations"]
                                old_user_data.save()
                            if "medical_debt" in dictionary.keys():
                                old_user_data.medical_debt = dictionary["medical_debt"]
                                old_user_data.save()
                                
                            dicc = {"id":real_user_id,"username":old_user_data.username,"password":old_user_data.password,
                            "name":old_user_data.name,"age":old_user_data.age,"psu_score":old_user_data.psu_score,
                            "university":old_user_data.university,"gpa_score":old_user_data.gpa_score,
                            "job":old_user_data.job,"salary":old_user_data.salary,"promotion":old_user_data.promotion,
                            "hospital":old_user_data.hospital,"operations":old_user_data.operations,"medical_debt":old_user_data.medical_debt}
                            json_response = json.dumps(dicc)
                            return HttpResponse(json_response, status=200)

                        else:
                            dicc = {"error": "invalid atributes"}
                            json_response = json.dumps(dicc)
                            return HttpResponseBadRequest(json_response, status=400)

                except:
                    dicc = {"error": "invalid atributes"}
                    json_response = json.dumps(dicc)
                    return HttpResponseBadRequest(json_response, status=400)

            else:
                dicc = {"error": "you do not have access to this resource"}
                json_response = json.dumps(dicc)
                return HttpResponse(json_response, status=403)   
        except:
            dicc = {"error": "invalid token"}
            json_response = json.dumps(dicc)
            return HttpResponse(json_response, status=401)

    else:
        try:
            incoming_token = request.headers["Authorization"]
            incoming_token = UserToken.objects.get(token=incoming_token).token
            real_user_object = UserToken.objects.get(token=incoming_token).user
            real_user_id = real_user_object.id
            incoming_url = request.path
            real_url = "/authyapp/users/" + f"{real_user_id}" 
            if str(real_url) == str(incoming_url):
                dicc = {"id":real_user_id,"username":real_user_object.username,"password":real_user_object.password,"name":real_user_object.name,"age":real_user_object.age,"psu_score":real_user_object.psu_score,"university":real_user_object.university,"gpa_score":real_user_object.gpa_score,"job":real_user_object.job,"salary":real_user_object.salary,"promotion":real_user_object.promotion,"hospital":real_user_object.hospital,"operations":real_user_object.operations,"medical_debt":real_user_object.medical_debt}
                json_response = json.dumps(dicc)
                return HttpResponse(json_response, status=200)

            else:
                dicc = {"error": "you do not have access to this resource"}
                json_response = json.dumps(dicc)
                return HttpResponse(json_response, status=403)                
        except:
                dicc = {"error": "invalid token"}
                json_response = json.dumps(dicc)
                return HttpResponse(json_response, status=401)

@csrf_exempt
def authorization_request(request):

    lista_scopes = ['basic','education','work','medical']
    random_string = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ1234567890"
    nonce = ""
    if request.method == 'GET':

        for i in range(0,20):
            pos = random.randint(0,len(random_string) - 1)
            char = random_string[pos]
            nonce = nonce + char

        # assigned regular string date
        now = dt.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        ano = int(str(dt_string[6:10]))
        mes = int(str(dt_string[3:5]))
        dia = int(str(dt_string[0:2]))
        hora = int(str(dt_string[11:13]))
        minuto = int(str(dt_string[14:16]))
        segundo = int(str(dt_string[17:19]))

        date_time = datetime.datetime(ano,mes,dia,hora,minuto,segundo)

        try:
            user_id = request.GET.getlist('user_id')
            user_id = int(user_id[0])

            try:
                scopes = request.GET.getlist('scopes')
                app_id = request.GET.getlist('app_id')

                scopes_full_string = scopes[0]
                scopes_list = scopes_full_string.split(',')
                print(scopes_list)

                for s in scopes_list:
                    if s not in lista_scopes:
                        print(s)
                        dicc = {"error": "invalid oauth request"}
                        json_response = json.dumps(dicc)
                        return HttpResponse(json_response, status=400)  


                grant_url = "/oauth/grant?" + f"user_id={user_id}&" + f"scopes={scopes[0]}&" + f"app_id={app_id[0]}&" + f"nonce={nonce}" 
                expiration = round(time.mktime(date_time.timetuple())) + 10
                dicc = {"message": f"{app_id[0]} está intentando acceder a basic,education, ¿desea continuar?", "grant_url":grant_url, "expiration": expiration}
                json_response = json.dumps(dicc)
                access_token_request = AccessTokenRequest(user_id=user_id,app_id=app_id[0],nonce=nonce,expiration=expiration)
                access_token_request.save()
                return HttpResponse(json_response, status=200)         

            except:
                dicc = {"error": "invalid oauth request"}
                json_response = json.dumps(dicc)
                return HttpResponse(json_response, status=400)  

        except: 
            dicc = {"error": "user not found"}
            json_response = json.dumps(dicc)
            return HttpResponse(json_response, status=404)  

@csrf_exempt
def authorization_accepted(request):
    #pusheesssss
    lista_scopes = ['basic','education','work','medical']

    if request.method == 'GET':
        try:
            user_id = request.GET.getlist('user_id')
            user_id = int(user_id[0])

            try: 
                app_id = request.GET.getlist('app_id')
                scopes = request.GET.getlist('scopes')
                nonce = request.GET.getlist('nonce')

                scopes_full_string = scopes[0]
                scopes_list = scopes_full_string.split(',')
                app_id = str(app_id[0])
                nonce = str(nonce[0])
                print(nonce)

                for s in scopes_list:
                    if s not in lista_scopes:
                        dicc = {"error": "invalid oauth grant"}
                        json_response = json.dumps(dicc)
                        return HttpResponse(json_response, status=400)  

                try:
                    incoming_token = request.headers["Authorization"]
                    incoming_token = UserToken.objects.get(token=incoming_token).token
                    real_user_object = UserToken.objects.get(token=incoming_token).user
                    real_user_id = real_user_object.id
                    if int(real_user_id) == int(user_id):
                        try:
                            req_uid = AccessTokenRequest.objects.get(user_id=real_user_id).user_id
                            req_timestamp = AccessTokenRequest.objects.get(user_id=real_user_id).expiration
                            req_nonce = AccessTokenRequest.objects.get(user_id=real_user_id).nonce
                            expiration = round(time.mktime(req_timestamp.timetuple()))
                            current_time = dt.now()
                            dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
                            ano = int(str(dt_string[6:10]))
                            mes = int(str(dt_string[3:5]))
                            dia = int(str(dt_string[0:2]))
                            hora = int(str(dt_string[11:13]))
                            minuto = int(str(dt_string[14:16]))
                            segundo = int(str(dt_string[17:19])) 
                            current_date_time = datetime.datetime(ano, mes, dia, hora, minuto, segundo)
                            current_time = round(time.mktime(current_date_time.timetuple()))
                            print(str(nonce))
                            if (current_time - expiration) <= 10 and str(req_nonce) == str(nonce):
                                access_token = UserToken.objects.get(user_id=real_user_id).token
                                access_token_create = AccessToken(user_id=user_id,app_id=app_id,scopes=scopes_full_string ,expiration=current_time+60)
                                access_token_create.save()
                                dicc = {"access_token": access_token, "expiration": expiration }
                                json_response = json.dumps(dicc)
                                return HttpResponse(json_response, status=200)
                            else:
                                print(current_time - expiration)
                                dicc = {"error": "invalid authorization grant"}
                                json_response = json.dumps(dicc)
                                return HttpResponse(json_response, status=406)                            
                        except:
                            dicc = {"error": "invalid authorization grant"}
                            json_response = json.dumps(dicc)
                            return HttpResponse(json_response, status=406)
                    else:
                        dicc = {"error": "invalid token"}
                        json_response = json.dumps(dicc)
                        return HttpResponse(json_response, status=401)

                except:
                    dicc = {"error": "invalid token"}
                    json_response = json.dumps(dicc)
                    return HttpResponse(json_response, status=401)
                

            except:
                dicc = {"error": "invalid oauth grant"}
                json_response = json.dumps(dicc)
                return HttpResponse(json_response, status=400)      

        except: 
            dicc = {"error": "user not found"}
            json_response = json.dumps(dicc)
            return HttpResponse(json_response, status=403)      

@csrf_exempt
def basic(request, user_id):
    if request.method == 'GET':
        try:
            incoming_token = request.headers["Authorization"]
            incoming_token = UserToken.objects.get(token=incoming_token).token
            incoming_scopes = AccessToken.objects.get(token=incoming_token).scopes
            scopes_list = incoming_scopes.split(',')
            real_user_object = UserToken.objects.get(token=incoming_token).user
            real_user_id = real_user_object.id
            incoming_url = request.path
            real_url = "/authyapp/users/" + f"{real_user_id}" + "/basic"
            if str(real_url) == str(incoming_url) and "basic" in scopes_list:
                return HttpResponse("No content", status=200)

            else:
                dicc = {"error": "you do not have access to this resource"}
                json_response = json.dumps(dicc)
                return HttpResponse(json_response, status=403)   
        except:
            dicc = {"error": "invalid token"}
            json_response = json.dumps(dicc)
            return HttpResponse(json_response, status=401)

@csrf_exempt
def basic(request, user_id):
    if request.method == 'GET':
        try:
            incoming_token = request.headers["Authorization"]
            incoming_token = UserToken.objects.get(token=incoming_token).token
            incoming_scopes = AccessToken.objects.get(token=incoming_token).scopes
            scopes_list = incoming_scopes.split(',')
            real_user_object = UserToken.objects.get(token=incoming_token).user
            real_user_id = real_user_object.id
            incoming_url = request.path
            real_url = "/authyapp/users/" + f"{real_user_id}" + "/basic"
            if str(real_url) == str(incoming_url) and "basic" in scopes_list:
                return HttpResponse("No content", status=200)

            else:
                dicc = {"error": "you do not have access to this resource"}
                json_response = json.dumps(dicc)
                return HttpResponse(json_response, status=403)   
        except:
            dicc = {"error": "invalid token"}
            json_response = json.dumps(dicc)
            return HttpResponse(json_response, status=401)

@csrf_exempt
def medical(request, user_id):
    if request.method == 'GET':
        try:
            incoming_token = request.headers["Authorization"]
            incoming_token = UserToken.objects.get(token=incoming_token).token
            incoming_scopes = AccessToken.objects.get(token=incoming_token).scopes
            scopes_list = incoming_scopes.split(',')
            real_user_object = UserToken.objects.get(token=incoming_token).user
            real_user_id = real_user_object.id
            incoming_url = request.path
            real_url = "/authyapp/users/" + f"{real_user_id}" + "/medical"
            if str(real_url) == str(incoming_url) and "medical" in scopes_list:
                return HttpResponse("No content", status=200)

            else:
                dicc = {"error": "you do not have access to this resource"}
                json_response = json.dumps(dicc)
                return HttpResponse(json_response, status=403)   
        except:
            dicc = {"error": "invalid token"}
            json_response = json.dumps(dicc)
            return HttpResponse(json_response, status=401)

@csrf_exempt
def work(request, user_id):
    if request.method == 'GET':
        try:
            incoming_token = request.headers["Authorization"]
            incoming_token = UserToken.objects.get(token=incoming_token).token
            incoming_scopes = AccessToken.objects.get(token=incoming_token).scopes
            scopes_list = incoming_scopes.split(',')
            real_user_object = UserToken.objects.get(token=incoming_token).user
            real_user_id = real_user_object.id
            incoming_url = request.path
            real_url = "/authyapp/users/" + f"{real_user_id}" + "/work"
            if str(real_url) == str(incoming_url) and "work" in scopes_list:
                return HttpResponse("No content", status=200)

            else:
                dicc = {"error": "you do not have access to this resource"}
                json_response = json.dumps(dicc)
                return HttpResponse(json_response, status=403)   
        except:
            dicc = {"error": "invalid token"}
            json_response = json.dumps(dicc)
            return HttpResponse(json_response, status=401)

@csrf_exempt
def education(request, user_id):
    if request.method == 'GET':
        try:
            incoming_token = request.headers["Authorization"]
            incoming_token = UserToken.objects.get(token=incoming_token).token
            incoming_scopes = AccessToken.objects.get(token=incoming_token).scopes
            scopes_list = incoming_scopes.split(',')
            real_user_object = UserToken.objects.get(token=incoming_token).user
            real_user_id = real_user_object.id
            incoming_url = request.path
            real_url = "/authyapp/users/" + f"{real_user_id}" + "/education"
            if str(real_url) == str(incoming_url) and "education" in scopes_list:
                return HttpResponse("No content", status=200)

            else:
                dicc = {"error": "you do not have access to this resource"}
                json_response = json.dumps(dicc)
                return HttpResponse(json_response, status=403)   
        except:
            dicc = {"error": "invalid token"}
            json_response = json.dumps(dicc)
            return HttpResponse(json_response, status=401)
